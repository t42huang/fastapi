#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 09/06/24 19:23
# @Author  : tina.huanght@shopee.com
# @File    : dependencies.py
from fastapi import Header, HTTPException

async def get_token_header(x_token: str = Header()):
    if x_token != "test":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="NO Jessica token provided.")