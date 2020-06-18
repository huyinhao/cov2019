## cov2019疫情追踪

### Python使用flask、echarts框架，搭配Mysql数据库

## 更新历史
* ### 4月1日更新海外各国的数据源, 新增境外输入、无症状感染者数据
* ### 4月11日更新国内境外输入城市排行

## 项目基本介绍

1、 爬虫爬取腾讯新闻数据并筛选关键数据

* 数据来源 
   
      https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5
      https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign
      https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=美国
      要查询各国，只需在'country='后替换国家名称即可

2、 使用Mysql建立数据库和关键表，存储爬取的数据

3、 使用flask框架，templates目录下存放html模板，
static目录存放各类静态文件
(static/css存放css样式，static/js存放js文件)

4、 使用 echarts 框架绘制

* 中国疫情地图、中国疫情趋势图、
* 全球疫情地图、全球疫情趋势图、
* 国内城市累计确诊排行图、国内累计境外输入省市排行、海外累计确诊排行图

5、 部署项目定时刷新页面数据，1小时使用一次爬虫刷新数据库数据，也可以手动ctrl+f5清除浏览器缓存达到刷新页面的效果

6、 启动项目前请仔细阅读注意事项！

***
### 基本函数名、文件名定义介绍

* ##### left--左侧、center--中部、right--右侧、top-left--左上侧、bottom-left--左下侧...
* ##### china--中国疫情地图、国内城市排行
* ##### china-trend--中国疫情累计趋势、新增趋势、累计境外输入省市排行
* ##### world--全球疫情地图
* ##### world-trend--海外疫情趋势，不含中国
 
***

## 注意事项（请仔细阅读!)

* 数据库相关操作封装于utils.py文件，连接数据库前，请仔细阅读下列注意事项

* 先建立一个数据库，名为 cov2019

* 建立history表，用于存放全国疫情历史数据

* 建立details表，用于存放当日全国各城市更新的疫情数据

* 建立fforeign表，用于存放海外疫情数据

* 建立global表，用于存放全球疫情趋势数据

> 上述所需建立表的sql语句，均存放于../database/tables.md文件中，也可以直接导入数据库
>> 旧版本数据库位于../database/更新前数据库/cov2019.sql 

>> 最新版本数据库位于../database/4月1日更新数据库/cov2019.sql

* 当然可以自行修改表名，只需要修改utils模块中所有涉及的sql语句中相应的表名

* 因此不推荐自定义表名

* 第一次启动项目(执行app.py)若出现报错，提示数据不存在，是因为数据库操作还未执行，数据表内容为空，属于正常现象

* 等待出现提示"数据库更新数据成功"后，重新启动项目就解决了

* 全球各国历史数据量比较大, 因此更新fforeign表需要等待一会

* 数据更新若未生效，可能是缓存的原因，在浏览器中按 ctrl+f5 可以清除缓存

* 下面具体介绍各模块

*** 

## 模块介绍

### utils模块

* 封装了所有的数据库操作和获取数据的方法

* 获取国内、海外最近的一次更新时间 -- get_time_china, get_time_global

* 数据库连接操作
    
    * 连接、关闭数据库 -- get_conn，close_conn

* 数据库更新操作
    
    * 更新history表，更新历史疫情数据  -- update_history
    
    * 更新details表，更新当日疫情数据  -- update_details
    
    * 更新fforeign表，更新海外疫情数据  -- update_fforeign
    
    * 更新global表，更新海外疫情数据  -- update_global

* 数据库查询操作
    * 进行sql查询 -- query
    * 获取china左侧数据，中国疫情地图 -- get_china_left
    * 获取china右上侧数据，全国确诊、治愈、死亡、现有确诊、境外输入、无症状感染者的累计和新增数据 -- get_china_top_right
    * 获取china右下侧数据，国内累计确诊城市排行 -- get_china_bottom_right
    * 获取china-trend左上侧数据，全国累计确诊、疑似、治愈、死亡趋势图 -- get_china_trend_top_left
    * 获取china-trend中上侧数据，全国新增确诊、疑似趋势图 -- get_china_trend_top_center
    * 获取china-trend右上侧数据，全国新增治愈、死亡趋势图 -- get_china_trend_top_right
    * 获取china-trend左下侧数据，全国新增境外输入、无症状感染者趋势图 -- get_china_trend_bottom_left
    * 获取china-trend中下侧数据，国内累计境外输入省市排行 -- get_china_trend_bottom_center
    * 获取china-trend右下侧数据，国内累计境外输入省市排行饼图 -- get_china_trend_bottom_right
    * 获取world数据，世界疫情地图 -- get_world
    * 获取world-trend数据，海外累计确诊趋势 -- get_world_trend_top_left
    * 获取world-trend数据，海外累计治愈、死亡, 新增确诊趋势 -- get_world_trend_bottom_left
    * 获取world-trend数据，海外国家累计确诊排行 -- get_world_trend_right
***

### spider模块 -- 爬虫

* 获取腾讯新闻数据，筛选并返回疫情的历史数据、当日数据、海外数据、境外输入数据
* 请求全国历史、全国当日、全球数据 -- get_url
* 返回全国历史数据 -- get_history_data 
* 返回当日国内各省数据 -- get_details_data 
* 请求某国的数据 -- get_url_country 
* 返回全球各国的历史数据 -- get_country_data 
* 返回全球的累计数据 -- get_global_data 
* 返回境外输入、无症状感染者数据 -- get_import_case
***

### app模块 -- 路由介绍

* #### 模板
    * 主页，即中国疫情地图、国内城市排行 -- '/'
    
    * 中国疫情累计趋势、新增趋势, 累计境外输入省市排行 -- '/china-trend'
    
    * 世界疫情地图 -- '/world'
    
    * 海外疫情趋势, 海外国家累计确诊排行-- '/world-trend'
       
* #### 数据库

    * 刷新数据库各表数据 -- '/update_china', '/update_china_trend', '/update_world', '/update_world_trend'

* #### 数据获取    
    * 获取国内、海外最近的一次更新时间 -- get_time_china, get_time_global
    
    * china页-中国各省累计确诊数据 -- '/get_china_left'
    
    * china页-国内累计确诊疑似、治愈、死亡人数 -- '/get_china_top_right'
    
    * china页-国内累计确诊城市排行 -- '/get_china_bottom_right'
    
    * china-trend页-中国累计确诊、疑似、治愈、死亡趋势 -- '/get_china_trend_top_left'
    
    * china-trend页-中国新增确诊、疑似趋势 -- '/get_china_trend_top_center'
    
    * china-trend页-中国新增治愈、死亡趋势 -- '/get_china_trend_top_right'
    
    * china-trend页-中国新增境外输入、无症状感染者趋势 -- '/get_china_trend_bottom_left'
    
    * china-trend页-国内累计境外输入省市排行 -- '/get_china_trend_bottom_center'
    
    * china-trend页-国内累计境外输入省市排行饼图 -- '/get_china_trend_bottom_right'
    
    * world页-世界疫情地图数据 -- '/get_world'
    
    * world-trend页-海外累计确诊、治愈、死亡，新增确诊趋势 -- '/get_world_trend_left'
    
    * world-trend页-海外累计确诊排行 -- '/get_world_trend_right'

***

## 静态文件介绍

* 各页面模板 
    * china.html, china-trend.html, world.html, world-trend.html
    * 位于templates目录
    
* jquery资源 
    * jquery.min.js

* echarts资源 
    * echarts.min.js, dark.js

* 控制各页面数据的动态获取 
    * china-controller.js
    * china-trend-controller.js
    * world-controller.js
    * world-trend-controller.js

* 中国疫情地图相关
    * china.js, china-left.js
    
* 除湖北省外城市累计确诊排行 
    * china-bottom-right.js

* 中国累计确诊、疑似、治愈、死亡趋势
    * china-trend-top-left.js
    
* 中国累计境外输入、无症状感染者趋势
    * china-trend-bottom-left.js

* 中国新增确诊、疑似趋势
    * china-trend-top-center.js
    
* 中国新增治愈、死亡趋势
    * china-trend-top-right.js
    
* 累计境外输入省市排行
    * china-trend-bottom-center.js
    * china-trend-bottom-right.js

* 世界疫情地图
    * world.js, world-map.js
    
* 海外累计确诊、治愈、死亡以及新增趋势
    * world-trend-top-left.js
    * world-trend-top-right.js

* 海外累计确诊排行数据图
    * world-trend-right.js
***  
## 效果预览

### 4.1日更新

![imgs view1](https://github.com/huyinhao/cov2019/blob/master/imgs/view1.png)

![imgs view2](https://github.com/huyinhao/cov2019/blob/master/imgs/view2.png)

![imgs view3](https://github.com/huyinhao/cov2019/blob/master/imgs/view3.png)

![imgs view4](https://github.com/huyinhao/cov2019/blob/master/imgs/view4.png)