from async_robot_lib import module
import asyncio
import datetime

async def asleep_without_await(time, id):
    # This will not block/wait but print out
    # after right away
    print(f"{id} before asleep_without_await = {datetime.datetime.now()}")
    asyncio.sleep(time)
    print(f"{id} after asleep_without_await = {datetime.datetime.now()}")

async def asleep_with_await(time, id):
    # This will actually block/wait and not print out after
    # until the sleep is done
    print(f"{id} before asleep_without_await = {datetime.datetime.now()}")
    await asyncio.sleep(time)
    print(f"{id} after asleep_without_await = {datetime.datetime.now()}")


async def asleep_with_await_and_new_task_after_finish(time, id, tg: asyncio.TaskGroup):
    # This will actually block/wait and not print out after
    # until the sleep is done
    print(f"{id} before asleep_without_await = {datetime.datetime.now()}")
    await asyncio.sleep(time)
    print(f"{id} after asleep_without_await = {datetime.datetime.now()}")
    tg.create_task(asleep_with_await(1, 'x'))


async def longfunction():
    await asyncio.sleep(1)
    result = 10
    return result

def synch_callback(fut: asyncio.Future):
    if not fut.cancelled() and fut.done():
        print(f"longfunction finished={fut.result()}")
    else:
        print("No results")


async def main():
    ## show that coroutine must be awaited
    #await asleep_without_await(1, '1')
    #await asleep_without_await(1, '2')

    ## show that await leads to sequential
    ## execution
    #await asleep_with_await(1, '1')
    #await asleep_with_await(1, '2')

    ## show that two coroutines can run in parallel
    # async with asyncio.TaskGroup() as tg:
    #     task1 = tg.create_task(asleep_with_await(1, '1'))
    #     task2 = tg.create_task(asleep_with_await(1, '2'))
    # print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")


    ## tasks can be added while task group is running
    ## by adding task group to a coroutine
    # async with asyncio.TaskGroup() as tg:
    #     task1 = tg.create_task(asleep_with_await(1, '1'))
    #     task2 = tg.create_task(asleep_with_await_and_new_task_after_finish(1, '2', tg))
    # print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")

    ## tasks can have associated callbacks
    ## which are called after completion
    # task = asyncio.create_task(longfunction())
    # task.add_done_callback(synch_callback)
    # await asyncio.wait_for(task, None)

    ## tasks can be cancelled
    ## either explicitly by task.cancel()
    ## or implicitly when a timeout occurs in wait
    task = asyncio.create_task(longfunction())
    task.add_done_callback(synch_callback)
    wait_time = .5
    try:
        r = await asyncio.wait_for(task, wait_time)
    except asyncio.TimeoutError as ex:
        print(f"timeout={ex}")
    else:
        print(f"All work done fine: {r}")
    finally:
        print("App finished!")
    


asyncio.run(main())
