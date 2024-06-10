#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 09/06/24 18:42
# @Author  : tina.huanght@shopee.com
# @File    : main.py.py

from fastapi import Depends, FastAPI
from .routers import users, items
from .internal import admin

from .dependencies import get_query_token

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)

app.include_router(admin.router,
                   prefix="/admin",
                   tags=["admin"],
                   dependencies=[Depends(get_query_token)],
                   responses={418: {"description": "this is admin"}})

@app.get("/")
async def root():
    return {"message": "this is a framework"}

