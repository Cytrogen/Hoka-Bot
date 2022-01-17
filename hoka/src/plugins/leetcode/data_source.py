import json
import logging
import requests
import nonebot.log


LEETCODE_URL="https://leetcode-cn.com/problemset/all/"
base_url = 'https://leetcode-cn.com'


def get_leetcode_question_everyday()->str:
    try:
        resp = requests.get(url=LEETCODE_URL)
        response = requests.post(base_url + "/graphql", json={
            "operationName": "questionOfToday",
            "variables": {},
            "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
        })

        leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get(
            'questionTitleSlug')

        url = base_url + "/problems/" + leetcodeTitle
        response = requests.post(base_url + "/graphql",
                                 json={"operationName": "questionData", "variables": {"titleSlug": leetcodeTitle},
                                       "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
       
        jsonText = json.loads(response.text).get('data').get("question")
        no = jsonText.get('questionFrontendId')
        leetcodeTitle = jsonText.get('translatedTitle')
        level = jsonText.get('difficulty')
        context = jsonText.get('translatedContent')
        return json.dumps(jsonText)
    except Exception as ex:
        raise ex