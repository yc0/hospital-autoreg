# Hospital-autoreg
Help you register your preferred doctors
幫助您掛號，掛到您理想的醫生

## Description
I've moved out all sensitive data/urls from perplexing for hospitals.
Therefore, it is sort of concepts (actually it's workable)

我己經移掉所有敏感的資訊包含網路位址，避免醫院的困擾
但他仍然具有參考價值(它真的可以運行)

## Features 特色
- lightweigh 輕量
- multi-threading 多執行緒
- framework-free 免框架 (no-scrapy, no-selenium)

## Prerequisite
```
pip install requests
```

## Manual 使用方式
```
python ar.py -i A1234567890 -s 外科 -mm 01 -dd 01 -dr 都凱傑'

```

* __-i --id__
  * your identification in Taiwan
  * 您台灣身份證
* __-w --week__
  * (bool) within this week ?
  * (bool) 是掛本周的嗎？
  * value = [true | false]
* __-v --verbose__
  * verbose
  * 詳細流程
  * -vv -vvv with different levels of logs
- __-s --section__
  * sections of departments
  * 掛號科別
  * 可輸入關鍵字 (partial match)
- __-mm --month__
  * your month of birthday
  * 生日月份
- __-dd --date__
  * your date of birthday
  * 生日日期
- __-dr --doctor__
  * your prefered doctor' name
  * 欲掛號之醫生姓名