class Object:
    @staticmethod
    def return_obj(chat_id=None,text=None,photo=None,reply_markup=None,message_id=None,media=None,data=None):
        obj = {'chat_id': chat_id}
        if data:
            obj['chat_id']=data['chat_id']
        if media:
            obj['media']=media
        if photo:
            obj['photo']=photo
            obj['caption'] = text
        elif text:
            obj['text']=text
        if reply_markup:
            obj['reply_markup']=reply_markup
        if message_id:
            obj['message_id']=message_id
        obj['disable_web_page_preview']= True
        return obj
