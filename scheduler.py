# import aioschedule

# import asyncio

# from quotes import MotivationalQuote


# async def schedule_func():
#     try:
#         # aioschedule.every().day.at("08:30").do(MotivationalQuote.get_quote())
#         aioschedule.every(10).seconds.do(MotivationalQuote.get_quote())
#         while True:
#             await aioschedule.run_pending()
#             await asyncio.sleep(5)

#     except Exception as error:
#         print(error)
