#strasbourg: all 14 a8 nodes are working


experiment_conf = {
    "job_name": "EnOSlib",
    "walltime": "03:15",
    "resources": {
        "machines": [
            # --------- STRASBOURG --------- 

            #strasbourg PAN 0
        #    {
        #         "roles": ["m3_strasbourg_0"],
        #         "hostname" : [
        #             "m3-40.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-15.iotlab",

        #     },
        #     {
        #         "roles": ["br_strasbourg_0"],
        #         #"archi": "m3:at86rf231",
        #         "hostname" : [
        #             "m3-41.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-15.iotlab",
        #     },
        #     #strasbourg PAN 1
        #     {
        #         "roles": ["m3_strasbourg_1"],
        #         "hostname" : [
        #             "m3-42.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-16.iotlab",

        #     },
        #     {
        #         "roles": ["br_strasbourg_1"],
        #         "hostname" : [
        #             "m3-43.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-16.iotlab",
        #     },
        #     #strasbourg PAN 2
        #     {
        #         "roles": ["m3_strasbourg_2"],
        #         "hostname" : [
        #             "m3-44.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-19.iotlab",
        #     },
        #     {
        #         "roles": ["br_strasbourg_2"],
        #         "hostname" : [
        #             "m3-45.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-19.iotlab",
        #     },
        #     #strasbourg PAN 3
        #     {
        #         "roles": ["m3_strasbourg_3"],
        #         "hostname" : [
        #             "m3-46.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-20.iotlab",
        #     },
        #     {
        #         "roles": ["br_strasbourg_3"],
        #         "hostname" : [
        #             "m3-47.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-20.iotlab",
        #     },


            #Strasbourg A8
           { 
                "roles": ["a8_strasbourg_1"],
                "hostname" : [
                    "a8-1.strasbourg.iot-lab.info",
                    "a8-2.strasbourg.iot-lab.info",
                    "a8-3.strasbourg.iot-lab.info",
                    "a8-4.strasbourg.iot-lab.info",
                    "a8-5.strasbourg.iot-lab.info",
                    "a8-6.strasbourg.iot-lab.info",
                    "a8-7.strasbourg.iot-lab.info",
                    "a8-8.strasbourg.iot-lab.info",
                    "a8-9.strasbourg.iot-lab.info",
                    "a8-10.strasbourg.iot-lab.info",
                    "a8-11.strasbourg.iot-lab.info",
                    "a8-12.strasbourg.iot-lab.info",
                    "a8-13.strasbourg.iot-lab.info",
                    "a8-14.strasbourg.iot-lab.info",
                ],
           },

        #alternative strasbourg
         #strasbourg PAN 0



        #    {
        #         "roles": ["m3_strasbourg_0"],
        #         "hostname" : [
        #             "m3-40.strasbourg.iot-lab.info",
        #             "m3-41.strasbourg.iot-lab.info",
        #             "m3-42.strasbourg.iot-lab.info",
        #             "m3-43.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-15.iotlab",

        #     },
        #     {
        #         "roles": ["br_strasbourg_0"],
        #         #"archi": "m3:at86rf231",
        #         "hostname" : [
        #             "m3-44.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-15.iotlab",
        #     },
        #     #strasbourg PAN 1
        #     {
        #         "roles": ["m3_strasbourg_1"],
        #         "hostname" : [
        #             "m3-20.strasbourg.iot-lab.info",
        #             "m3-21.strasbourg.iot-lab.info",
        #             "m3-22.strasbourg.iot-lab.info",
        #             "m3-23.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-16.iotlab",

        #     },
        #     {
        #         "roles": ["br_strasbourg_1"],
        #         "hostname" : [
        #             "m3-24.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-16.iotlab",
        #     },
        #     #strasbourg PAN 2
        #     {
        #         "roles": ["m3_strasbourg_2"],
        #         "hostname" : [
        #             "m3-31.strasbourg.iot-lab.info",
        #             "m3-32.strasbourg.iot-lab.info",
        #             "m3-33.strasbourg.iot-lab.info",
        #             "m3-34.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-19.iotlab",
        #     },
        #     {
        #         "roles": ["br_strasbourg_2"],
        #         "hostname" : [
        #             "m3-35.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-19.iotlab",
        #     },
        #     #strasbourg PAN 3
        #     {
        #         "roles": ["m3_strasbourg_3"],
        #         "hostname" : [
        #             "m3-52.strasbourg.iot-lab.info",
        #             "m3-53.strasbourg.iot-lab.info",
        #             "m3-54.strasbourg.iot-lab.info",
        #             "m3-55.strasbourg.iot-lab.info",
        #         ],
        #         "image": "hello-world-20.iotlab",
        #     },
        #     {
        #         "roles": ["br_strasbourg_3"],
        #         "hostname" : [
        #             "m3-56.strasbourg.iot-lab.info",
        #         ],
        #         "image": "border-router-20.iotlab",
        #     },


        #     #Strasbourg A8
        #    { 
        #         "roles": ["a8_strasbourg"],
        #         "hostname" : [
        #             "a8-8.strasbourg.iot-lab.info",
        #             "a8-9.strasbourg.iot-lab.info",
        #         ],
        #    },


            # --------- SACLAY ----------

             { #Successful and complete 45 nodes/ room for 3 more
                "roles": ["a8_saclay_1"],
                #"archi": "a8:at86rf231",
                "hostname": [
                'a8-1.saclay.iot-lab.info',
                'a8-10.saclay.iot-lab.info',
                'a8-103.saclay.iot-lab.info',
                'a8-106.saclay.iot-lab.info',
                'a8-11.saclay.iot-lab.info',
                'a8-14.saclay.iot-lab.info',
                'a8-16.saclay.iot-lab.info',
                'a8-17.saclay.iot-lab.info',
                'a8-2.saclay.iot-lab.info',
                'a8-31.saclay.iot-lab.info',
                'a8-34.saclay.iot-lab.info',
                'a8-36.saclay.iot-lab.info',
                'a8-38.saclay.iot-lab.info',
                'a8-39.saclay.iot-lab.info',
                'a8-40.saclay.iot-lab.info',
                'a8-41.saclay.iot-lab.info',
                'a8-42.saclay.iot-lab.info',
                'a8-43.saclay.iot-lab.info',
                'a8-44.saclay.iot-lab.info',
                'a8-45.saclay.iot-lab.info',
                'a8-46.saclay.iot-lab.info',
                'a8-47.saclay.iot-lab.info',
                'a8-48.saclay.iot-lab.info',
                'a8-5.saclay.iot-lab.info',
                'a8-61.saclay.iot-lab.info',
                'a8-62.saclay.iot-lab.info',
                'a8-63.saclay.iot-lab.info',
                'a8-64.saclay.iot-lab.info',
                'a8-66.saclay.iot-lab.info',
                'a8-67.saclay.iot-lab.info',
                'a8-69.saclay.iot-lab.info',
                'a8-70.saclay.iot-lab.info',
                'a8-71.saclay.iot-lab.info',
                'a8-72.saclay.iot-lab.info',
                'a8-73.saclay.iot-lab.info',
                'a8-74.saclay.iot-lab.info',
                'a8-75.saclay.iot-lab.info',
                'a8-76.saclay.iot-lab.info',
                'a8-77.saclay.iot-lab.info',
                'a8-78.saclay.iot-lab.info',
                'a8-79.saclay.iot-lab.info',
                'a8-87.saclay.iot-lab.info',
                'a8-90.saclay.iot-lab.info',
                'a8-91.saclay.iot-lab.info',
                'a8-92.saclay.iot-lab.info',
                ]
            },

            # --------- GRENOBLE --------- 

        #     #Grenoble PAN 0
        #    {
        #         "roles": ["m3_grenoble_0"],
        #         "hostname" : [
        #             "m3-272.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-21.iotlab",

        #     },
        #     {
        #         "roles": ["br_grenoble_0"],
        #         "hostname" : [
        #             "m3-273.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-21.iotlab",
        #     },
        #     #Grenoble PAN 1
        #     {
        #         "roles": ["m3_grenoble_1"],
        #         "hostname" : [
        #             "m3-274.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-22.iotlab",

        #     },
        #     {
        #         "roles": ["br_grenoble_1"],
        #         "hostname" : [
        #             "m3-275.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-22.iotlab",
        #     },
        #     #Grenoble PAN 2
        #     {
        #         "roles": ["m3_grenoble_2"],
        #         "hostname" : [
        #             "m3-318.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-24.iotlab",
        #     },
        #     {
        #         "roles": ["br_grenoble_2"],
        #         "hostname" : [
        #             "m3-319.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-24.iotlab",
        #     },
        #     #Grenoble PAN 3
        #     {
        #         "roles": ["m3_grenoble_3"],
        #         "hostname" : [
        #             "m3-321.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-25.iotlab",
        #     },
        #     {
        #         "roles": ["br_grenoble_3"],
        #         "hostname" : [
        #             "m3-320.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-25.iotlab",
        #     },

        

        #Alternative Grenoble
         #Grenoble PAN 0
        #    {
        #         "roles": ["m3_grenoble_0"],
        #         "hostname" : [
        #             "m3-103.grenoble.iot-lab.info",
        #             "m3-104.grenoble.iot-lab.info",
        #         #    "m3-105.grenoble.iot-lab.info",
        #         #    "m3-106.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-21.iotlab",

        #     },
        #     {
        #         "roles": ["br_grenoble_0"],
        #         "hostname" : [
        #             "m3-107.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-21.iotlab",
        #     },
        #     #Grenoble PAN 1
        #     {
        #         "roles": ["m3_grenoble_1"],
        #         "hostname" : [
        #             "m3-108.grenoble.iot-lab.info",
        #             "m3-109.grenoble.iot-lab.info",
        #        #     "m3-110.grenoble.iot-lab.info",
        #         #    "m3-111.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-22.iotlab",

        #     },
        #     {
        #         "roles": ["br_grenoble_1"],
        #         "hostname" : [
        #             "m3-112.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-22.iotlab",
        #     },
        #     #Grenoble PAN 2
        #     {
        #         "roles": ["m3_grenoble_2"],
        #         "hostname" : [
        #             #"m3-113.grenoble.iot-lab.info",
        #             "m3-114.grenoble.iot-lab.info",
        #           #  "m3-115.grenoble.iot-lab.info",
        #          #   "m3-116.grenoble.iot-lab.info",
        #         ],
        #         "image": "hello-world-24.iotlab",
        #     },
        #     {
        #         "roles": ["br_grenoble_2"],
        #         "hostname" : [
        #             "m3-117.grenoble.iot-lab.info",
        #         ],
        #         "image": "border-router-24.iotlab",
        #     },
            #Grenoble PAN 3
            # {
            #     "roles": ["m3_grenoble_3"],
            #     "hostname" : [
            #        #"m3-120.grenoble.iot-lab.info",
            #        "m3-121.grenoble.iot-lab.info",
            #        #"m3-122.grenoble.iot-lab.info",
            #       # "m3-123.grenoble.iot-lab.info",
            #     ],
            #     "image": "hello-world-25.iotlab",
            # },
            # {
            #     "roles": ["br_grenoble_3"],
            #     "hostname" : [
            #         "m3-124.grenoble.iot-lab.info",
            #     ],
            #     "image": "border-router-25.iotlab",
            # },

            # Grenoble a8

             { #185 nodes, room for 4 more
                "roles": ["a8_grenoble_1"],
                #"archi": "a8:at86rf231",
                #"site": "grenoble",
                "hostname": [
                    'a8-1.grenoble.iot-lab.info',
                    'a8-10.grenoble.iot-lab.info',
                    'a8-103.grenoble.iot-lab.info',
                    'a8-104.grenoble.iot-lab.info',
                    'a8-105.grenoble.iot-lab.info',
                    'a8-106.grenoble.iot-lab.info',
                    'a8-107.grenoble.iot-lab.info',
                    'a8-108.grenoble.iot-lab.info',
                    'a8-109.grenoble.iot-lab.info',
                    'a8-11.grenoble.iot-lab.info',
                    'a8-110.grenoble.iot-lab.info',
                    'a8-112.grenoble.iot-lab.info',
                    'a8-113.grenoble.iot-lab.info',
                    'a8-115.grenoble.iot-lab.info',
                    'a8-116.grenoble.iot-lab.info',
                    'a8-117.grenoble.iot-lab.info',
                    'a8-118.grenoble.iot-lab.info',
                    'a8-119.grenoble.iot-lab.info',
                    'a8-12.grenoble.iot-lab.info',
                    'a8-120.grenoble.iot-lab.info',
                    'a8-121.grenoble.iot-lab.info',
                    'a8-122.grenoble.iot-lab.info',
                    'a8-123.grenoble.iot-lab.info',
                    'a8-124.grenoble.iot-lab.info',
                    'a8-125.grenoble.iot-lab.info',
                    'a8-126.grenoble.iot-lab.info',
                    'a8-127.grenoble.iot-lab.info',
                    'a8-128.grenoble.iot-lab.info',
                    'a8-129.grenoble.iot-lab.info',
                    'a8-13.grenoble.iot-lab.info',
                    'a8-131.grenoble.iot-lab.info',
                    'a8-133.grenoble.iot-lab.info',
                    'a8-134.grenoble.iot-lab.info',
                    'a8-135.grenoble.iot-lab.info',
                    'a8-136.grenoble.iot-lab.info',
                    'a8-137.grenoble.iot-lab.info',
                   # 'a8-138.grenoble.iot-lab.info',
                    'a8-139.grenoble.iot-lab.info',
                    'a8-14.grenoble.iot-lab.info',
                    'a8-142.grenoble.iot-lab.info',
                    'a8-144.grenoble.iot-lab.info',
                    'a8-146.grenoble.iot-lab.info',
                    'a8-147.grenoble.iot-lab.info',
                    'a8-15.grenoble.iot-lab.info',
                    'a8-150.grenoble.iot-lab.info',
                    'a8-151.grenoble.iot-lab.info',
                    'a8-152.grenoble.iot-lab.info',
                    'a8-153.grenoble.iot-lab.info',
                    'a8-154.grenoble.iot-lab.info',
                    'a8-155.grenoble.iot-lab.info',
                    'a8-156.grenoble.iot-lab.info',
                    'a8-157.grenoble.iot-lab.info',
                    'a8-16.grenoble.iot-lab.info',
                    'a8-161.grenoble.iot-lab.info',
                    'a8-162.grenoble.iot-lab.info',
                    'a8-163.grenoble.iot-lab.info',
                    'a8-165.grenoble.iot-lab.info',
                    'a8-166.grenoble.iot-lab.info',
                    'a8-168.grenoble.iot-lab.info',
                    'a8-169.grenoble.iot-lab.info',
                    'a8-17.grenoble.iot-lab.info',
                    'a8-170.grenoble.iot-lab.info',
                    'a8-171.grenoble.iot-lab.info',
                    'a8-173.grenoble.iot-lab.info',
                    #'a8-174.grenoble.iot-lab.info',
                    'a8-175.grenoble.iot-lab.info',
                    'a8-176.grenoble.iot-lab.info',
                    'a8-177.grenoble.iot-lab.info',
                    'a8-179.grenoble.iot-lab.info',
                    'a8-18.grenoble.iot-lab.info',
                    'a8-180.grenoble.iot-lab.info',
                    'a8-181.grenoble.iot-lab.info',
                    'a8-182.grenoble.iot-lab.info',
                    'a8-183.grenoble.iot-lab.info',
                    'a8-184.grenoble.iot-lab.info',
                    'a8-185.grenoble.iot-lab.info',
                    'a8-187.grenoble.iot-lab.info',
                    'a8-188.grenoble.iot-lab.info',
                    'a8-189.grenoble.iot-lab.info',
                    'a8-19.grenoble.iot-lab.info',
                    'a8-190.grenoble.iot-lab.info',
                    'a8-191.grenoble.iot-lab.info',
                    'a8-192.grenoble.iot-lab.info',
                    'a8-193.grenoble.iot-lab.info',
                    'a8-194.grenoble.iot-lab.info',
                    'a8-195.grenoble.iot-lab.info',
                    ]
            },

            { 
                "roles": ["a8_grenoble_2"],
                "hostname" : [
                    'a8-197.grenoble.iot-lab.info',
                    'a8-198.grenoble.iot-lab.info',
                    'a8-199.grenoble.iot-lab.info',
                    'a8-200.grenoble.iot-lab.info',
                    'a8-201.grenoble.iot-lab.info',
                    'a8-202.grenoble.iot-lab.info',
                    'a8-203.grenoble.iot-lab.info',
                    'a8-204.grenoble.iot-lab.info',
                    'a8-205.grenoble.iot-lab.info',
                    'a8-206.grenoble.iot-lab.info',
                    'a8-207.grenoble.iot-lab.info',
                    'a8-208.grenoble.iot-lab.info',
                    'a8-209.grenoble.iot-lab.info',
                    'a8-210.grenoble.iot-lab.info',
                    'a8-211.grenoble.iot-lab.info',
                    'a8-212.grenoble.iot-lab.info',
                    'a8-213.grenoble.iot-lab.info',
                    'a8-214.grenoble.iot-lab.info',
                    'a8-215.grenoble.iot-lab.info',
                    'a8-216.grenoble.iot-lab.info',
                    'a8-217.grenoble.iot-lab.info',
                    'a8-218.grenoble.iot-lab.info',
                    'a8-219.grenoble.iot-lab.info',
                    'a8-22.grenoble.iot-lab.info',
                    'a8-220.grenoble.iot-lab.info',
                    'a8-221.grenoble.iot-lab.info',
                    'a8-222.grenoble.iot-lab.info',
                    'a8-223.grenoble.iot-lab.info',
                    'a8-224.grenoble.iot-lab.info',
                    'a8-225.grenoble.iot-lab.info',
                    'a8-226.grenoble.iot-lab.info',
                    'a8-227.grenoble.iot-lab.info',
                    'a8-228.grenoble.iot-lab.info',
                    'a8-23.grenoble.iot-lab.info',
                    'a8-24.grenoble.iot-lab.info',
                    'a8-25.grenoble.iot-lab.info',
                    'a8-27.grenoble.iot-lab.info',
                    'a8-29.grenoble.iot-lab.info',
                    'a8-3.grenoble.iot-lab.info',
                    'a8-30.grenoble.iot-lab.info',
                    'a8-31.grenoble.iot-lab.info',
                    'a8-33.grenoble.iot-lab.info',
                    'a8-34.grenoble.iot-lab.info',
                    'a8-36.grenoble.iot-lab.info',
                    'a8-37.grenoble.iot-lab.info',
                    'a8-39.grenoble.iot-lab.info',
                    'a8-4.grenoble.iot-lab.info',
                    'a8-40.grenoble.iot-lab.info',
                    'a8-41.grenoble.iot-lab.info',
                    'a8-42.grenoble.iot-lab.info',
                    'a8-43.grenoble.iot-lab.info',
                    'a8-44.grenoble.iot-lab.info',
                    'a8-45.grenoble.iot-lab.info',
                    'a8-46.grenoble.iot-lab.info',
                    'a8-47.grenoble.iot-lab.info',
                    'a8-48.grenoble.iot-lab.info',
                    'a8-49.grenoble.iot-lab.info',
                    'a8-5.grenoble.iot-lab.info',
                    'a8-50.grenoble.iot-lab.info',
                    'a8-51.grenoble.iot-lab.info',
                    'a8-52.grenoble.iot-lab.info',
                    'a8-53.grenoble.iot-lab.info',
                    'a8-57.grenoble.iot-lab.info',
                    'a8-58.grenoble.iot-lab.info',
                    'a8-59.grenoble.iot-lab.info',
                    'a8-61.grenoble.iot-lab.info',
                    'a8-62.grenoble.iot-lab.info',
                    'a8-63.grenoble.iot-lab.info',
                    'a8-64.grenoble.iot-lab.info',
                    'a8-65.grenoble.iot-lab.info',
                    'a8-66.grenoble.iot-lab.info',
                    'a8-67.grenoble.iot-lab.info',
                    'a8-68.grenoble.iot-lab.info',
                    'a8-69.grenoble.iot-lab.info',
                    'a8-7.grenoble.iot-lab.info',
                    'a8-70.grenoble.iot-lab.info',
                    'a8-71.grenoble.iot-lab.info',
                    'a8-73.grenoble.iot-lab.info',
                    'a8-74.grenoble.iot-lab.info',
                    'a8-79.grenoble.iot-lab.info',
                    'a8-8.grenoble.iot-lab.info',
                    'a8-80.grenoble.iot-lab.info',
                    'a8-81.grenoble.iot-lab.info',
                    'a8-82.grenoble.iot-lab.info',
                    'a8-83.grenoble.iot-lab.info',
                    'a8-84.grenoble.iot-lab.info',
                    'a8-85.grenoble.iot-lab.info',
                    'a8-86.grenoble.iot-lab.info',
                    'a8-88.grenoble.iot-lab.info',
                    'a8-89.grenoble.iot-lab.info',
                    'a8-9.grenoble.iot-lab.info',
                    'a8-90.grenoble.iot-lab.info',
                    'a8-93.grenoble.iot-lab.info',
                    'a8-94.grenoble.iot-lab.info',
                    'a8-95.grenoble.iot-lab.info',
                    'a8-96.grenoble.iot-lab.info',
                    'a8-97.grenoble.iot-lab.info',
                    'a8-98.grenoble.iot-lab.info',
                    'a8-99.grenoble.iot-lab.info',
                ],
           },
                
            { 
                "roles": ["rpi_grenoble_1"],
                "hostname" : [
                    "rpi3-1.grenoble.iot-lab.info",
                    "rpi3-2.grenoble.iot-lab.info",
                    "rpi3-3.grenoble.iot-lab.info",
                    "rpi3-4.grenoble.iot-lab.info",
                    "rpi3-5.grenoble.iot-lab.info",
                ],
           },

            #Grenoble rpi


            # --------- PARIS --------- 

            # #paris PAN 0
            # {
            #     "roles": ["m3_paris_0"],
            #     "hostname" : [
            #         "m3-47.paris.iot-lab.info",
            #         "m3-59.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_networking-11.elf",

            # },
            # {
            #     "roles": ["br_paris_0"],
            #     "hostname" : [
            #         "m3-48.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_border_router-11.elf",
            # },

            # #paris PAN 1

            # {
            #     "roles": ["m3_paris_1"],
            #     "hostname" : [
            #         "m3-41.paris.iot-lab.info",
            #         "m3-42.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_networking-12.elf",

            # },
            # {
            #     "roles": ["br_paris_1"],
            #     "hostname" : [
            #         "m3-40.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_border_router-12.elf",
            # },

            # #paris PAN 2

            # {
            #     "roles": ["m3_paris_2"],
            #     "hostname" : [
            #         "m3-44.paris.iot-lab.info",
            #         "m3-45.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_networking-13.elf",

            # },
            # {
            #     "roles": ["br_paris_2"],
            #     "hostname" : [
            #         "m3-43.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_border_router-13.elf",
            # },

            # #paris PAN 3


            # {
            #     "roles": ["m3_paris_3"],
            #     "hostname" : [
            #         "m3-62.paris.iot-lab.info",
            #         "m3-63.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_networking-14.elf",

            # },
            # {
            #     "roles": ["br_paris_3"],
            #     "hostname" : [
            #         "m3-60.paris.iot-lab.info",
            #     ],
            #     "image": "gnrc_border_router-14.elf",
            # },


            # { #All 14 s are working!
            #     "roles": ["a8_strasbourg"],
            #     "archi": "a8:at86rf231",
            #     "site": "strasbourg",
            #     "number": 14,
            # },

            { 
                "roles": ["a8_paris_1"],
                "hostname": [
                    'a8-1.paris.iot-lab.info',
                    'a8-11.paris.iot-lab.info',
                   # 'a8-12.paris.iot-lab.info',
                    'a8-13.paris.iot-lab.info',
                   # 'a8-15.paris.iot-lab.info',
                    'a8-16.paris.iot-lab.info',
                    'a8-17.paris.iot-lab.info',
                    'a8-18.paris.iot-lab.info',
                    'a8-19.paris.iot-lab.info',
                    'a8-2.paris.iot-lab.info',
                    'a8-20.paris.iot-lab.info',
                    'a8-21.paris.iot-lab.info',
                    'a8-22.paris.iot-lab.info',
                    'a8-23.paris.iot-lab.info',
                    'a8-24.paris.iot-lab.info',
                    'a8-25.paris.iot-lab.info',
                    'a8-26.paris.iot-lab.info',
                    'a8-27.paris.iot-lab.info',
                    'a8-28.paris.iot-lab.info',
                    'a8-29.paris.iot-lab.info',
                    'a8-3.paris.iot-lab.info',
                    'a8-30.paris.iot-lab.info',
                    'a8-32.paris.iot-lab.info',
                    'a8-33.paris.iot-lab.info',
                    'a8-34.paris.iot-lab.info',
                    'a8-35.paris.iot-lab.info',
                    'a8-36.paris.iot-lab.info',
                    'a8-37.paris.iot-lab.info',
                    'a8-38.paris.iot-lab.info',
                    'a8-39.paris.iot-lab.info',
                    'a8-4.paris.iot-lab.info',
                    'a8-40.paris.iot-lab.info',
                    #'a8-41.paris.iot-lab.info',
                    'a8-42.paris.iot-lab.info',
                    'a8-43.paris.iot-lab.info',
                    'a8-44.paris.iot-lab.info',
                    'a8-45.paris.iot-lab.info',
                    'a8-46.paris.iot-lab.info',
                    'a8-47.paris.iot-lab.info',
                    'a8-48.paris.iot-lab.info',
                    'a8-49.paris.iot-lab.info',
                    'a8-5.paris.iot-lab.info',
                    'a8-50.paris.iot-lab.info',
                    'a8-51.paris.iot-lab.info',
                    'a8-52.paris.iot-lab.info',
                    'a8-53.paris.iot-lab.info',
                    'a8-54.paris.iot-lab.info',
                    'a8-55.paris.iot-lab.info',
                    'a8-56.paris.iot-lab.info',
                    #'a8-57.paris.iot-lab.info',
                    'a8-58.paris.iot-lab.info',
                    'a8-59.paris.iot-lab.info',
                    'a8-6.paris.iot-lab.info',
                    'a8-60.paris.iot-lab.info',
                    'a8-61.paris.iot-lab.info',
                    'a8-62.paris.iot-lab.info',
                    'a8-7.paris.iot-lab.info',
                    'a8-9.paris.iot-lab.info'
                    ]
                },
            ]
        
    },
}