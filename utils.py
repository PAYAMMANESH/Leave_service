from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('4E4576356E4C5849717953535A324E4D634A7A754554736A456534634B30304F7A6833344C7666386670413D')
        params = {'sender': '09159114347',
                  'receptor': phone_number,
                  'message': f"{code}کد تایید شما "
                  }

        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
