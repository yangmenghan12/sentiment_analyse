container: dict[str, list] = {}  # key:事件类型  value:订阅事件的人[方法(接收事件类型的数据去使用)]


def subscribe(event_type: str, callback):
    """
    订阅的本质：将函数注册到对应类型的事件上
    :param event_type:
    :param callback:
    :return:
    """
    if event_type not in container:
        container[event_type] = []
    container[event_type].append(callback)

def tom_wechat(data):
    print(f"tom收到:{data}")

def jack_wechat(data):
    print(f"jack收到:{data}")

def publish(event_type: str, data: dict):
    """
    发布的本质：根据事件类型找到订阅事件类型的人(回调函数)
    :param event_type:
    :param data:
    :return:
    """
    if event_type in container:
        for callback in container[event_type]:
            callback(data)

subscribe("news", tom_wechat)
subscribe("weather", jack_wechat)
subscribe("news", jack_wechat)

# container  {"news":[tom_wechat,jack_wechat],"weather":[jack_wechat]}

# publish("news", "今天不用上班了！")
publish("weather", {"content":"今天天气真好","location":"Beijing"})

"""
场景1：订阅者：前端（渲染进度）  发布者：服务端(发送进度更新事件类型，事件更新的数据)：两端的通信（数据交互）前端、服务端
场景2：服务端与服务端的数据通信（并不是有多个服务）一个应用的多个服务的Agent进行数据通信   
1. 前端订阅某种事件类型   ---- > 服务端发送对应的事件类型，数据（进度更新） ---->3.前端就能使用 
面试题：
1. 多个Agent之间是如何进行数据通信的？
解法1：利用pub、sub机制。前端：Agent通信时的数据不能过多。一旦过多。缺点:OOM风险、不能持久化 优点：速度快
解法2：利用文件系统【优点：不存在内存占用问题、持久化】。缺点：速度急慢【文件IO】
平衡：文件系统读写速度<速度<内存读写速度       内存持久化<持久化<文件系统---->中间件【Redis[内存数据库、持久化机制【AOF/RDB】]、消息队列【Kafka/RabbitMQ、RocketMQ...】】
insight_agent  ---》 host_agent
insight_agent--->send("队列1",[发送数据])----->host_agent:consume("队列1")--->发送数据(处理):通信方式
"""