function load_line_chart(url, id) {
	var myChart = echarts.init(document.getElementById(id));
	$.get(url).done(function(result) {
		result = result.data
	    option = {
	    	    title: {
	    	        text: '任务消费情况折线图'
	    	    },
	    	    color:['#61a0a8', '#d48265', '#91c7ae', '#749f83'],
	    	    tooltip : {
	    	        trigger: 'axis',
	    	        axisPointer: {
	    	            type: 'cross',
	    	            label: {
	    	                backgroundColor: '#6a7985'
	    	            }
	    	        }
	    	    },
	    	    legend: {
	    	        data:['队列任务数', '抓取速度']
	    	    },
	    	    toolbox: {
	    	        feature: {
	    	            saveAsImage: {}
	    	        }
	    	    },
	    	    grid: {
	    	        left: '3%',
	    	        right: '4%',
	    	        bottom: '3%',
	    	        containLabel: true
	    	    },
	    	    xAxis : [
	    	        {
	    	            type : 'category',
	    	            boundaryGap : false,
	    	            data : result == null ? [] : result.date
	    	        }
	    	    ],
	    	    yAxis : [
	    	        {
	    	            type : 'value'
	    	        }
	    	    ],
	    	    series : [
	    	        {
	    	            name:'队列任务数',
	    	            type:'line',
	    	            stack: '总量',
	    	            areaStyle: {normal: {}},
	    	            data:result == null ? [] : result.queue_data.data
	    	        },
	    	        {
	    	            name:'抓取速度',
	    	            type:'line',
	    	            stack: '个数',
	    	            areaStyle: {normal: {}},
	    	            data:result == null ? [] : result.speed_data.data
	    	        }
	    	    ]
	    	};
	    myChart.setOption(option);
	})
	//window.onresize = myChart.resize;
}

function load_table(url, id) {
	$.get(url).done(function(result) {
		if(result.status_code == 0) {
			var htmlStr = ""
			datas = result.data
			for(var i in datas) {
				queue_name = datas[i].queue_name
				tasks_count = datas[i].tasks_count
				if(tasks_count > 0) {
					htmlStr += "<tr class='text-c'>"
					htmlStr += "<td><a onclick=\"set_queue('" + queue_name + "', 1)\" title='查看消费情况'>" + queue_name + "</a></td>"
					htmlStr += "<td>" + tasks_count + "</td>"
				}else {
					htmlStr += "<tr class='text-c' style='display:none' mark='zero'>"
					htmlStr += "<td><a onclick=\"set_queue('" + queue_name + "', 1)\" title='查看消费情况'>" + queue_name + "</a></td>"
					htmlStr += "<td>" + tasks_count + "</td>"
				}
				htmlStr += "</tr>"
			}
			htmlStr += "<tr class='text-c' mark='show'>"
			htmlStr += "<td colspan='2'><a onclick=\"show_queues('" + id + "')\" title='查看空队列'>查看更多</a></td>"
			htmlStr += "</tr>"
			htmlStr += "<tr class='text-c' style='display:none' mark='hide'>"
			htmlStr += "<td colspan='2'><a onclick=\"hide_queues('" + id + "')\" title='隐藏空队列'>隐藏空队列</a></td>"
			htmlStr += "</tr>"
			$("#" + id).html(htmlStr)
		}
	})
}

function show_queues(container) {
	$("#" + container).find("tr[mark='zero']").show()
	$("#" + container).find("tr[mark='show']").hide()
	$("#" + container).find("tr[mark='hide']").show()
}

function hide_queues(container) {
	$("#" + container).find("tr[mark='zero']").hide()
	$("#" + container).find("tr[mark='show']").show()
	$("#" + container).find("tr[mark='hide']").hide()
}


