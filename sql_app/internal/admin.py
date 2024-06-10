#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 09/06/24 19:24
# @Author  : tina.huanght@shopee.com
# @File    : admin.py
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}