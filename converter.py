from mdutils import MdUtils
import markdown
import os
from datetime import datetime


# 병원 DB연동을 가정하고 가져왔다치는 회원 정보
dummy_data = {
    "hospital": "창원경상국립대학교병원",
    "department": "정형외과",
    "name": "주한새",
    "sex": "남",
    "birthYear": 1998,
    "birthMonth": 7,
    "birthDay": 15
}




def convert(req_dict):
    doc_title = f'{dummy_data["hospital"]} {dummy_data["department"]} 환자 예진표'
    filename = f'{dummy_data["name"]}_{dummy_data["birthYear"]}_{dummy_data["birthMonth"]:02d}'
    mdFile = MdUtils(file_name=filename, title=doc_title)
    # 기본정보 불러와서 쓰기
    duration_category = ['3일 이내', '7일 이내', '1개월 이내', '3개월 이내', '1년 이내', '1년 이상']
    name = dummy_data['name']
    sex = dummy_data['sex']
    birthday = f"{dummy_data['birthYear']}/{dummy_data['birthMonth']}/{dummy_data['birthDay']}"
    symptom_duration = duration_category[int(req_dict["duration"])] # 인덱스 변환
    mdFile.new_header(level=1, title='1. 기본 정보')
    mdFile.new_paragraph(f'이름(성별): {name}({sex})')
    mdFile.new_paragraph(f'생년월일: {birthday}')
    mdFile.new_paragraph(f'증상 발생 시점: {symptom_duration}')
    

    # 건강정보 불러와서 쓰기
    body_parts = req_dict["details"]
    mdFile.new_header(level=1, title='2. 건강 정보')
    mdFile.new_header(level=2, title=f'통증 부위 (통증 정도: {req_dict["pain"]})')
    mdFile.new_list(body_parts)

    # MEPS test 시행 여부 확인해서 조건부 표 작성
    if "stability" in req_dict:
        mdFile.new_header(level=2, title=f'MEPS 테스트 결과')
        # 고통정도 -> MEPS 고통점수 환산
        pain_score = 45 - int(req_dict["pain"])*9 
        # elbow 각도 -> MEPS motion 점수 환산
        elbow_angle = int(req_dict["motion"])
        motion_score = 0 + 15*(elbow_angle >= 50) + 5*(elbow_angle >= 100)
        # MEPS stability 점수 - 그대로
        stability_score = int(req_dict["stability"])
        # MEPS function 점수 리스트 길이*5
        function_score = 5*len(req_dict["elbowFunction"])
        # 총점 및 평가 라벨
        total_score = sum([pain_score, motion_score, stability_score, function_score])
        labels = ['Poor', 'Fair', 'Good', 'Excellent']
        idx = 0 + (total_score > 59) + (total_score > 74) + (total_score > 89)
        table = ['Category', 'Score']
        table.extend(['Pain Intensity', f'{pain_score}'])
        table.extend(['Motion', f'{motion_score}'])
        table.extend(['Stability', f'{stability_score}'])
        table.extend(['Function', f'{function_score}'])
        table.extend(['**총점**', f'**{total_score} ({labels[idx]})**'])
        mdFile.new_table(columns=2, rows = 6, text=table, text_align='left')


    recent_diagnosis = req_dict["diagnosisDuration"]
    mdFile.new_header(level=1, title=f'3. 병력 (최근 진단: {recent_diagnosis})')
    mdFile.new_list([req_dict["diagnosis"]])

    etc = []
    if req_dict["medicine"] != "아니요":
        etc.append("약을 복용 중인 환자로, 안전한 처방을 위해 환자분에게 복용 중인 약의 봉투 등을 지참하도록 안내하였음")
    if len(etc) == 0:
        etc.append("해당 없음")
    mdFile.new_header(level=1, title='4. 특이사항')
    mdFile.new_list(etc)
    mdFile.create_md_file()


    today = datetime.today().strftime('%y%m%d')

    html_dir = f'{today}'
    if not os.path.isdir(html_dir):
        os.mkdir(html_dir)
    
    markdown.markdownFromFile(
    input=f'{filename}.md',
    output=f'{html_dir}/{filename}.html',
    encoding='utf8',
    extensions=[
             'markdown.extensions.tables',
             'markdown.extensions.sane_lists',
             'markdown.extensions.wikilinks',
             ]
    )

    return f'{html_dir}/{filename}.html'