var world_else = echarts.init(document.getElementById('world_else'),'dark')

var world_else_option = {
    title:{
        text:'海外新增确诊、治愈、死亡趋势',
        textStyle:{
			fontSize:20,
			color:'#D4F2E7',
		},
		left:'2%',
        top:'0%'
	},
    backgroundColor:'#333',
    tooltip:{
        trigger:'axis',
		axisPointer:{
			type:'line',
			lineStyle:{
				color:'#7171C6'
			}
		},
        textStyle:{
            fontSize : 14,
        } ,
    },
	legend:{
		data:['累计死亡','新增确诊'],
		textStyle:{
            fontSize : 14,
			color:'#D4F2E7',
        } ,
        top:'0%',
		left:'right',
	},
	//图形位置
	grid: {
		left: '10%',
		right:'2.6%',
        top:'10%',
		bottom:'6%',
		containLable:true,

	},
	xAxis: [{
	    type:'category',
		data:['01.20','01.21','01.22'],

	}],
	yAxis: [{
		type:'value',
		axisLabel:{
			show:true,
			color:'#D4F2E7',
			fontSize:14,
			formatter: function(value){
				if(value >= 1000)
				{
					value = value / 1000 + 'k'
				}
				return value;
			}
		},
		axisLine:{
			show:true,
		},
		splitLine:{
			show:true,
			lineStyle:{
				color:['#83bff6','#D4F2E7','#25F8CB','#EACD76'],
				width:2,
				type:'solid',
			}
		}
	}],
	series:[
	{
		name:'累计死亡',
		type:'line',
		smooth:true,
		data:[6,9,17]
	},
	{
		name:'新增确诊',
		type:'line',
		smooth:true,
		data:[6,9,17]
	}],
};

world_else.setOption(world_else_option)
