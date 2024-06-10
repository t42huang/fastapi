#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 09/06/24 19:24
# @Author  : tina.huanght@shopee.com
# @File    : users.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}