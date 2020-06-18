var countryRank = echarts.init(document.getElementById('countryRank'),'dark')

var seriesLabel = {
    normal: {
        show: true,
        textBorderColor: '#434343',
        textBorderWidth: 3
    }
}

countryRank_option = {
    title: {
        text: '海外疫情排行',
        left: 'right' ,
        top:'3%',
        textStyle:{
            fontSize: 21,
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['累计确诊', '累计治愈', '累计死亡'],
        left:'6%',
        top:'3%',
        textStyle:{
            fontSize : 16,
        } ,
    },
    grid: {
        left: 60,
        bottom:30,
        right:'3%'
    },

    xAxis: {
        type: 'value',
        name: '人',
        axisLabel: {
            formatter: '{value}'
        }
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['意大利', '伊朗', '韩国'],
        axisLabel:{
            fontSize : 16,
        } ,
    },
    series: [
        {
            name: '累计确诊',
            type: 'bar',
            data: [165, 170, 30],
            label: seriesLabel,
        },
        {
            name: '累计治愈',
            type: 'bar',
            label: seriesLabel,
            data: [150, 105, 110],
            markPoint: {
                symbolSize: 1,
                symbolOffset: [0, '50%'],
                label: {
                    // formatter: '{a|累计治愈}\n{b|{b} }{c|{c}}',
                    formatter: '{b|{b} }{c|{c}}',
                    backgroundColor: 'rgb(242,242,242)',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    // padding: [4, 10],
                    lineHeight: 26,
                    shadowBlur: 15,
                    shadowColor: '#000',
                    shadowOffsetX: 0,
                    shadowOffsetY: 1,
                    position: 'right',
                    distance: 110,
                    width:200,
                    height:20,
                    align:'center',
                    rich: {
                        a: {
                            align: 'center',
                            color: '#fff',
                            fontSize: 14,
                            textShadowBlur: 2,
                            textShadowColor: '#000',
                            textShadowOffsetX: 0,
                            textShadowOffsetY: 1,
                            textBorderColor: '#333',
                            textBorderWidth: 2
                        },
                        b: {
                            color: '#333',
                            fontSize:14
                        },
                        c: {
                            color: '#ff8811',
                            textBorderColor: '#000',
                            textBorderWidth: 1,
                            fontSize: 14
                        }
                    }
                },
                data: [
                    {type: 'max', name: '累计治愈MAX:'},
                ]
            }
        },
        {
            name: '累计死亡',
            type: 'bar',
            label: seriesLabel,
            data: [220, 82, 63],
            markPoint: {
                symbolSize: 1,
                symbolOffset: [0, '50%'],
                label: {
                    // formatter: '{a|累计死亡}\n{b|{b} }{c|{c}}',
                    formatter: '{b|{b} }{c|{c}}',
                    backgroundColor: 'rgb(242,242,242)',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    // padding: [4, 10],
                    lineHeight: 26,
                    shadowBlur: 15,
                    shadowColor: '#000',
                    shadowOffsetX: 0,
                    shadowOffsetY: 1,
                    position: 'right',
                    distance: 100,
                    width:180,
                    height:20,
                    align:'center',
                    rich: {
                        // a: {
                        //     align: 'center',
                        //     color: '#fff',
                        //     fontSize: 14,
                        //     textShadowBlur: 2,
                        //     textShadowColor: '#000',
                        //     textShadowOffsetX: 0,
                        //     textShadowOffsetY: 1,
                        //     textBorderColor: '#333',
                        //     textBorderWidth: 2
                        // },
                        b: {
                            color: '#333',
                            fontSize:14
                        },
                        c: {
                            color: '#ff8811',
                            textBorderColor: '#000',
                            textBorderWidth: 1,
                            fontSize: 14
                        }
                    }
                },
                data: [
                    {type: 'max', name: '累计死亡MAX:'},
                ]
            }
        }
    ]
};

countryRank.setOption(countryRank_option)