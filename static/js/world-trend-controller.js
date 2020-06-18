// 更新时间戳
function get_time(){
    $.ajax({
        url:'/get_time_global',
        timeout: 10000,
        success:function (data) {
            $('#time').html(data)
        },error:function () {

        }
    })
}

//更新数据库(history、details、fforeign三张表)
function update_sql(){
    $.ajax({
        url:'/update_world_trend',
        success:function (data) {

        },error:function () {

        }
    })
}

// 更新国外趋势图
function get_world_trend_left() {
    $.ajax({
        url:'/get_world_trend_left',
        success:function(data){
            world_confirm_option.xAxis[0].data = data.day
            world_confirm_option.series[0].data = data.confirm
            world_confirm_option.series[1].data = data.heal
            world_confirm.setOption(world_confirm_option)

            world_else_option.xAxis[0].data = data.day
            world_else_option.series[0].data = data.dead
            world_else_option.series[1].data = data.confirm_add
		    world_else.setOption(world_else_option)
        },
        error:function f() {

        }
    })
}

// 更新国外疫情排行
function get_world_trend_right() {
    $.ajax({
        url:'/get_world_trend_right',
        success:function(data){
            countryRank_option.yAxis.data = data.country
            countryRank_option.series[0].data = data.confirm
            countryRank_option.series[1].data = data.heal
            countryRank_option.series[2].data = data.dead
		    countryRank.setOption(countryRank_option)
        },
        error:function f() {

        }
    })
}

//访问时获取数据
update_sql();
get_time();
get_world_trend_left();
get_world_trend_right();
//停留页面时每一小时刷新一次数据
setInterval(update_sql,1000*60*60);
setInterval(get_time,1000*60*60);
setInterval(get_world_trend_left,1000*60*60);
setInterval(get_world_trend_right,1000*60*60);