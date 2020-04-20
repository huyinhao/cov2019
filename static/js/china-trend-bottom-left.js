var r1 = echarts.init(document.getElementById('r1'),'dark')

var r1_option = {
    title:{
        text:'全国境外输入、无症状感染者趋势',
        textStyle:{
			fontSize:22,
		},
		left:'left',
	},
    tooltip:{
        trigger:'axis',
		axisPointer:{
			type:'line',
			lineStyle:{
				color:'#7171C6'
			}
		},
    },
	legend:{
		data:['累计境外输入','累计无症状感染者'],
		left:'right',
		top:'8%',
		textStyle:{
            fontSize : 14,
        } ,
	},
	//图形位置
	grid: {
		left: '8%',
		right:'4%',
		bottom:'8%',
		top:50,
		containLable:true
	},
	xAxis: [{
	    type:'category',
		data:['01.20','01.21','01.22']
	}],
	yAxis: [{
		type:'value',
		axisLabel:{
			show:true,
			color:'white',
			fontSize:12,
			formatter: function(value){
				if(value >= 1000)
				{
					value = value / 1000 + 'k'
				}
				return value;
			}
		},
		axisLine:{
			show:true
		},
		splitLine:{
			show:true,
			lineStyle:{
				color:['#82ccdd','#b8e994','#78e08f','#38ada9','#079992'],
				width:1,
				type:'solid',
			}
		}
	}],
	series:[{
		name:'累计境外输入',
		type:'line',
		smooth:true,
		color:'#a55eea',
		data:[260,406,529]
	},{
		name:'累计无症状感染者',
		type:'line',
		smooth:true,
		color:'#eb3b5a',
		data:[52,37,3935]
	}]
};

r1.setOption(r1_option)
