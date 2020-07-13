xPaths = {
    # home page
    'acp_cookie': '/html/body/div[2]/div/a[2]',
    'dny_cookie': '/html/body/div[2]/div/a[1]',
    'login_name': '//*[@id="inputName"]',
    'login_lang': '//*[@id="loginLanguage"]',
    'login_play': '//*[@id="formLogin"]/button[1]',
    'create': '//*[@id="buttonLoginCreatePrivate"]',
    # create game lobby
    'lobby_play': '//*[@id="buttonLobbyPlay"]',
    'set_rounds': '//*[@id="lobbySetRounds"]',
    'set_times': '//*[@id="lobbySetDrawTime"]',
    'lobby_lang': '//*[@id="lobbySetLanguage"]',
    'custom_wds': '//*[@id="lobbySetCustomWords"]',
    'cus_wds_ex': '//*[@id="lobbyCustomWordsExclusive"]',
    # in game
    'html': '/html',
    'curr_word': '//*[@id="currentWord"]',
    'draw_pad': '//*[@id="canvasGame"]',
    'clear': '//*[@id="buttonClearCanvas"]',
    'pen': '//*[@id="containerBoard"]/div[2]/div[3]/div[1]/img',
    'brush': '//*[@id="containerBoard"]/div[2]/div[3]/div[2]/img',
    'fill': '//*[@id="containerBoard"]/div[2]/div[3]/div[3]/img',
    'size6': '//*[@id="containerBoard"]/div[2]/div[4]/div[1]/div/div',
    'size16': '//*[@id="containerBoard"]/div[2]/div[4]/div[2]/div/div',
    'size30': '//*[@id="containerBoard"]/div[2]/div[4]/div[3]/div/div',
    'size44': '//*[@id="containerBoard"]/div[2]/div[4]/div[4]/div/div',
}
# colors options
color_xPath = {
    4: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[3]',  # EF130B (red)
    10: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[6]',  # 00CC00 (green)
    14: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[8]',  # 231FD3 (blue)
    8: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[5]',  # FFE400 (yellow)
    16: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[9]',  # A300BA (purple)
    20: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[11]',  # A0522D (brown)
    12: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[7]',  # 00B2FF (sky blue)
    1: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[1]',  # 000    (black)
    # 0: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[1]',  # FFF
    2: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[2]',  # C1C1C1 (grey)
    3: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[2]',  # 4C4C4C (d grey)
    5: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[3]',  # 740B07 (d red)
    6: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[4]',  # FF7100 (orange)
    7: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[4]',  # C23800
    9: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[5]',  # E8A200
    11: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[6]',  # 005510
    13: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[7]',  # 00569E
    15: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[8]',  # 0E0865
    17: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[9]',  # 550069
    18: '//*[@id="containerBoard"]/div[2]/div[2]/div[1]/div[10]',  # D37CAA
    19: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[10]',  # A75574
    21: '//*[@id="containerBoard"]/div[2]/div[2]/div[2]/div[11]',  # 63300D
}

draw_pad_loc = {
    'x0': 470,
    'y0': 270,
    'xn': 1250,
    'yn': 870,
}

# '''   # x path for avatar looks selection
# # color
# //*[@id="loginAvatar"]/div[1]
# <div class="color" style="background-size: 960px 960px; background-position: -480px -96px;"></div>
# color_arrow_left = '//*[@id="loginAvatarArrowsLeft"]/div[3]'
#
# # eyes
# //*[@id="loginAvatar"]/div[2]
# <div class="eyes" style="background-size: 960px 960px; background-position: -96px -96px;"></div>
# eyes_arrow_left = '//*[@id="loginAvatarArrowsLeft"]/div[1]'
#
# //*[@id="loginAvatar"]/div[3]
# <div class="mouth" style="background-size: 960px 960px; background-position: -192px 0px;"></div>
# mouth_arrow_left = '//*[@id="loginAvatarArrowsLeft"]/div[2]'
# '''
