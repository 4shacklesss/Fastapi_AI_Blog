from fastapi import FastAPI, Request, HTTPException, status, Depends

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError

#from fastapi.responses import JSONResponse

from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler

from starlette.exceptions import HTTPException as StarletteHTTPException

from routers import posts, users
#remove schemas

from typing import Annotated

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload

from database import Base, engine, get_db

from contextlib import asynccontextmanager



import models

#Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # start up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    #shut down
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates") #what we creates in folder, object for our file

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])


## home
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).order_by(models.Post.date_posted.desc()))#returning a list of post, and we sort it from latest to oldest
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )

## post_page
@app.get("/posts/{post_id}", include_in_schema=False)
async def post_page(request: Request, post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")







#=================================
## user_posts_page
@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id)
        .order_by(models.Post.date_posted.desc()),
    )
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )
#===============================


#---- delete

## login and register template_routes
@app.get("/login", include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"title": "Login"},
    )


@app.get("/register", include_in_schema=False)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"title": "Register"},
    )

@app.get("/account", include_in_schema=False)
async def account_page(request: Request):
    return templates.TemplateResponse(
        request,
        "account.html",
        {"title": "Account"},
    )
## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    

    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)
    
    message = (
            exception.detail
            if exception.detail
            else "An error occurred. Please check your request and try again."
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
    
## this is for handle case beside ints   validation
@app.exception_handler(RequestValidationError)
async def general_exception_handler(request: Request, exception: RequestValidationError):
    
    if request.url.path.startswith("/api"):
        return await Request_validationError_exception_handlers(request, exception)
    
    ##html response   
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code":status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again"
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )