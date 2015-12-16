# Dump data to readable JSON format
def dump(data):
  try:
    return json.dumps(data, indent=2)
  except:
    return data

def pdump(data):
    print(dump(data))

