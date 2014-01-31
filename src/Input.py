class Input:

  data = None

  def __init__(self):
    pass

  def __len__(self):
    return len(self.data)

  def copy(self):
    assert(False)

class Arg(Input):
  def __init__(self, i, data):
    self.i = i
    
    self.data = str(data)
    if ("\0" in data):
      self.data = self.data.split("\0")[0]

    self.size = len(self.data)

  def GetData(self):
    return str(self.data)

  def GetSize(self):
    return len(self.data)

  def PrepareData(self):

    return self.GetData()

  def IsValid(self):
    return self.size > 0

  def __cmp__(self, arg):
    return cmp(self.i, arg.i)

  def copy(self):
    return Arg(self.i, self.data)

  def GetName(self):
    return "argv_"+str(self.i)

  def GetType(self):
    return "arg"


class Env(Input):
  def __init__(self, name, data):
    self.name = name

    self.data = str(data)
    if ("\0" in data):
      self.data = self.data.split("\0")[0]

    self.size = len(self.data)

  def GetData(self):
    return str(self.data)

  def GetSize(self):
    return len(self.data)

  def PrepareData(self):

    return self.GetData()

  def IsValid(self):
    return self.size > 0

  def __cmp__(self, arg):
    return cmp(self.i, arg.i)

  def copy(self):
    return Arg(self.i, self.data)

  def GetName(self):
    return "env_"+str(self.i)

  def GetType(self):
    return "env"

class File(Input):
  def __init__(self, filename, data):
    self.filename = str(filename)
    self.data = str(data)
    self.size = len(data)

  def GetData(self):
    return str(self.data)

  def GetSize(self):
    return len(self.data)

  def PrepareData(self):
    if self.filename == "/dev/stdin":
      with open("Stdin", 'w') as f:
        f.write(self.data)

      return "< Stdin"
    else:
      with open(self.filename, 'w') as f:
        f.write(self.data)

      return None

  def IsValid(self):
    return True

  def copy(self):
    return File(self.filename, self.data)

  def GetName(self):
    return "file_"+self.filename.replace("/", "__")

  def GetType(self):
    return "file"
