format1 = {}
format1["text"] = "What do you want to know?"
format1["fallback"] = "You are unalbe to press button"
format1["callback_id"] = "worng_products"
format1["color"] = "#3AA3E3"
format1["attachment_type"] = "default"
format1["actions"] = [{
                    "name": "product",
                    "text": "Get the list of popular products?          ",
                    "type": "button",
                    "value": "product",
                    "confirm": {
                        "title": "Using keyword \"OO (카테고리) , 인기\"",
                        "text": "It's showing top ten category's products  ex.) 의류 인기순위 보여줘 "
                                "       카테고리 목록 : 인기, 의류, 잡화, 브랜드패션",
                        "ok_text": "I Got it!",
                        # "dismiss_text": "No"
                    }
                },
                {
                    "name": "prices",
                    "text": "Get the products of prices?              ",
                    "type": "button",
                    "value": "prices",
                    "confirm": {
                        "title": "Using keyword \"OO (카테고리), 가격\"",
                        "text": "It's showing top ten category's products with price ex.) 의류 가격 보여줘",
                        "ok_text": "I Got it!",
                        # "dismiss_text": "No"
                    }
                },
                {
                    "name": "pricessort",
                    "text": "Can I set the oder?              ",
                    "type": "button",
                    "value": "pricessort",
                    "confirm": {
                        "title": "keyword \"낮은가격순 or 높은가격순\"",
                        "text": "It's showing product in the order of low/high prices                "
                                "                  ex.) 의류 낮은가격순으로 보여줘",
                        "ok_text": "I Got it!",
                        # "dismiss_text": "No"
                    }
                },
                {
                    "name": "review",
                    "text": "Can I find the rate of the product?                 ",
                    "type": "button",
                    "value": "review",
                    "confirm": {
                        "title": "Using \"OO (순위 또는 공란), 평점\"",
                        "text": "** For using this function, you should search the list before **                 "
                                "      ex.) 1위 평점 보여줘 / 평점 보여줘",
                        "ok_text": "I Got it!",
                        # "dismiss_text": "No"
                    }
                },
                {
                    "name": "search",
                    "text": "Can I search products?              ",
                    "type": "button",
                    "value": "search",
                    "confirm": {
                        "title": "Using \"OO 검색해줘\"",
                        "text": "It's showing OO 's searching result  ex.) 장갑 검색해줘",
                        "ok_text": "I Got it!",
                        # "dismiss_text": "No"
                    }
                },
            ]

