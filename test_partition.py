import faust


app = faust.App('my_test', key_serializer='raw', value_serializer='raw')
message_topic = app.topic('my_topic', key_type=bytes, value_type=bytes, partitions=4, internal=True)


@app.agent(message_topic)
async def mystream(stream: faust.Stream):
    async for e in stream.events():
        # print(message_topic.partitions)
        print(e.message.partition)


@app.agent(message_topic)
async def straek(stream: faust.Stream):
    async for s in stream.filter(lambda x: x == b"z"):
        print(s)
    # async for k, v in stream.items():
    #     print(k)
    #     print(v)


@app.timer(2.0, on_leader=True)
async def ppub():
    # await message_topic.send(key=b"a", value=b"x", partition=0)
    await message_topic.send(key=b"b", value=b"y", partition=1)
    await message_topic.send(key=b"c", value=b"z", partition=2)
    # await message_topic.send(key=b"d", value=b"w", partition=3)
