def validate(resp):
  """Validates that a response came back valid"""
  if resp != None:
    try:
      jr = resp.json()
      if jr['ok']:
        return jr
      else:
        print("Response, but not okay: {}".format(dump(jr)))
        return jr

    except:
      print("Response: {}".format(resp))
      print("Body: {}".format(resp.text))
      return resp

  else:
    print("No response!") # That's weird
    print("Response: {}".format(resp))
    print("Body: {}".format(resp.text))
    return None

