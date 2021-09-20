#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os
import sqlite3

from Bio import SeqIO
from pyppeteer import launch

progs = ['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx']
width, height = 1920, 1080


async def main(file, prog):
    browser = await launch(
        executablePath='D:/env/pyppeteer/local-chromium/588429/chrome-win32/chrome.exe',  # 启动chrome的路径
        headless=False,  # 关闭无头浏览器模式
        args=[
            f'--window-size={width},{height}',
            '--disable-infobars',  # 关闭自动化提示框
            '--no-sandbox',  # 关闭沙盒模式
            '--disable-gpu',  # 禁用GPU
            # '--start-maximized',  # 窗口最大化模式
        ]
    )
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    if prog not in progs:
        raise Exception('program error')
    await page.goto(f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM={prog}&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
    await page.screenshot({'path': 'ncbi.png'})
    page_text = await page.content()
    print(page_text)

    records = SeqIO.parse(file, format='fasta')
    print(f'读取序列文件')

    async for record in records:
        browser.find_element_by_id('seq').send_keys(record.seq.upper())
        browser.find_element_by_xpath('//*[@id="blastButton1"]/input').click()
    try:
        # (By.ID, 'dscTable')
        # browser.find_element_by_id('btndsConfig').click()
        # browser.find_element_by_xpath('//*[@id="dsConfig"]/li[3]/label').click()
        # browser.find_element_by_xpath('//*[@id="dsConfig"]/li[4]/label').click()
        # data = {'Sequence': self.record.id,
        #         'Description': table.find_element_by_xpath('//*/tr[1]/td[2]/span/a[@class="deflnDesc"]').text}
        return data
    except:
        print(f'Unknown: {record.id}')
    finally:
        # await asyncio.sleep(100)
        await browser.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(prog='blastn'))
