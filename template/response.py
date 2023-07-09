def Response(tipe, konten = None , title = None , description = None, upload = None):
    res = f"""
      tipe : {tipe}\nkonten : {konten}\ntitle : {title}\ndescription : {description}\nsubmit : /yieks
    """
    return res
  
def upload_response_text(username="anonimus"):
  return f'Halo suhu {username}\nmau upload konten apa nih!!'
