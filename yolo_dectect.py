import torch
import numpy as np
import yaml

class ImageDetect:
    model = model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5s', force_reload=True)
    data = {}
    # model(이미지)

    # 클래스 내에 정의된 함수들은 self 꼭 넣기
    
    # 클래스 생성 시 자동으로 호출되는 생성자 함수
    def __init__(self):
        with open('coco.yaml', 'r', encoding='UTF-8') as f:
            self.data = yaml.full_load(f)['names']

    # self : 사실 ImageDetect라는 뜻, 
    def detect_img(self, img): # img 부분에는 아무거나 써두댐, 심지어 한글도 가능
        # model(img) # 이건 위에있는 모델 못가르킴
        # self.model(img) # 이건 위에 있는 모델 가르킴
        result = self.model(img).xyxyn[0].numpy()
        return result