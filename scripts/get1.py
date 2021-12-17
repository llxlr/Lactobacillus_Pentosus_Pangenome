#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os

import aiosqlite
from Bio import SeqIO
from pyppeteer import launch

progs = ['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx']

def split(string):
    return map(lambda x: x[x.index(':')+1:], string.split(','))

async def main(db=None, file=None, prog='blastx', proxy=False):
    if prog not in progs:
        raise Exception('program error')
    browser = await launch(
        headless=False,  # 无头浏览器模式
        args=[
            '--disable-infobars',  # 关闭自动化提示框
            '--no-sandbox',  # 关闭沙盒模式
            '--disable-gpu',  # 禁用GPU
            '--start-maximized',  # 窗口最大化模式
            # f'--proxy-server={"127.0.0.1:11223" if proxy else ""}',  # 网络代理
        ]
    )
    page = await browser.newPage()
    await page.goto(f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM={prog}&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
    await asyncio.wait([
        page.content(),
        page.waitForNavigation({'timeout': 30000}),
    ])
    await page.screenshot({'path': 'ncbi.png'})
    # textarea = await page.querySelector('#seq')
    # print(textarea)

    await browser.close()
    # page_text = await page.content()
    # print(page_text)
    # await page.evaluate('() => document.getElementById("seq").value = ""')

    # records = SeqIO.parse(file, format='fasta')
    # print(f'读取序列文件')

    # async for record in records:
    #     # await page.type('#seq', record.seq.upper())
    #     # await page.click('#clearquery')
    #     # await page.click('#sopts > div.searchInfo.all > div.searchsummary > div > label')
    #     await page.click('#blastButton1 > input')
    # try:
    #     # (By.ID, 'dscTable')
    #     # browser.find_element_by_id('btndsConfig').click()
    #     # browser.find_element_by_xpath('//*[@id="dsConfig"]/li[3]/label').click()
    #     # browser.find_element_by_xpath('//*[@id="dsConfig"]/li[4]/label').click()
    #     # data = {'Sequence': self.record.id,
    #     #         'Description': table.find_element_by_xpath('//*/tr[1]/td[2]/span/a[@class="deflnDesc"]').text}
    #     return data
    # except:
    #     print(f'Unknown: {record.id}')
    # finally:
    #     # await asyncio.sleep(100)
    #     await browser.close()


if __name__ == '__main__':
    # file = "D:\\Projects\\PyCharmProjects\\Lactobacillus_Pentosus_Pangenome\\LP2\\seq\\HC2\\HC_Unique.fasta"
    # f_name = os.path.basename(file).replace('.fasta', '')

    # with open(file, 'r', encoding='utf-8') as handle:
    #     records = SeqIO.parse(handle, format='fasta')

    # gene_cluster_id, gene_caller_id = split('>gene_cluster_id:GC_00004526,gene_caller_id:1178')
    # print(gene_cluster_id, gene_caller_id)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
