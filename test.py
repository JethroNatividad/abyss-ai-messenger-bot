import pathlib
import textwrap
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("What is the meaning of life?")
print(response.text)

{'deltas': [{'attachments': [], 'body': '.abyss hey fucker', 'breadcrumbs': {}, 'data': {}, 'irisSeqId': '556', 'irisTags': ['entrypoint2:messenger_inbox:recent_threads', 'both_have_folder_assoc', 'IS_VALIDATED', 'did_not_update_iris_checkpoint', 'iris_post_process_decider_trace'], 'messageMetadata': {'actorFbId': '100008779424212', 'cid': {'canonicalParticipantFbids': ['100008779424212', '61554670604762']}, 'folderId': {'systemFolderId': 'INBOX'}, 'messageId': 'mid.$cAABtDsuDMA6S0kDsK2MoPujQ_a0m', 'offlineThreadingId': '7145029978482912550', 'tags': ['source:chat:light_speed', 'app_id:256002347743983'], 'threadKey': {'otherUserFbId': '100008779424212'}, 'threadReadStateEffect': 'MARK_UNREAD', 'threadSubtype': 1001, 'timestamp': '1703507895339', 'skipBumpThread': False}, 'requestContext': {'apiArgs': {}}, 'class': 'NewMessage'}], 'firstDeltaSeqId': 556, 'lastIssuedSeqId': 556, 'queueEntityId': 61554670604762}