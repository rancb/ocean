import sys
import csv
import copy
from numpy import zeros, savetxt

from src.Event    import Call, Crash, Abort, Exit, Signal, specs
from src.Types    import ptypes, isPtr, isNum, ptr32_ptypes, num32_ptypes, generic_ptypes


class Printer:
  def __init__(self, filename, pname):
    self.tests = set()
    self.file = open(filename, "a")
    self.pname = pname
    self.filters = []
    self.writer = csv.writer(self.file, delimiter='\t')

  def preprocess(self, event):

    r = set()
    if isinstance(event, Call):
      #print event.name, event.param_types, event.ret, event.retaddr, event.retvalue
      (name, args) = event.GetTypedName()

      #r.add((name+":ret_addr",str(args[0])))
      r.add((name+":ret_val",str(args[1])))

      for (index, arg) in enumerate(args[2:]):
        r.add((name+":"+str(index),str(arg)))
        #print r
    elif isinstance(event, Abort):
      (name, fields) = event.GetTypedName()
      r.add((name+":eip",str(fields[0])))
    
    elif isinstance(event, Exit):
      (name, fields) = event.GetTypedName()
      r.add((name,str(())))
    
    elif isinstance(event, Crash):
      (name, fields) = event.GetTypedName()
      r.add((name+":eip",str(fields[0])))

    elif isinstance(event, Signal):
      #assert(0)
      (name, fields) = event.GetTypedName()

      if name == "SIGSEGV":
        #print fields[0]
        r.add((name+":addr",str(fields[0])))
      else:
        r.add((name,str(fields[0])))

    return r

  def filter_by(self, filter_str):
    
    if '=' in filter_str:
      self.filters.append(tuple(filter_str.split('=')))
    else:
      print "Invalid fiter:", filter_str
  
  def print_events(self, module, events):
     
    r = list()

    for event in events:
      r = r + list(self.preprocess(event))
    
    events = r
     
    for x,y in events:
      #x,y = event
      print x+"="+y
      #assert(not ("abort" in str(x)))  

    print "\n",
    return


   
  def __print_events(self,module,delta,events):
   
    r = list()

    for event in events:
      r = r + list(self.preprocess(event))
    
    events = r

    if not (self.filters == [] or any(map(lambda f: f in events,self.filters))):
      return

    x = hash(tuple(events))
    if (x in self.tests):
      return

    self.tests.add(x)
    print module+"\t"+str(delta)+"\t", 
    for x,y in events:
      #x,y = event
      print x+"="+y+" ",
      #assert(not ("abort" in str(x)))  

    print "\n",
    return


class DataPrinter:
  def __init__(self, filename,pname,classes):
    self.tests = set()
    self.file = open(filename, "a")
    self.pname = pname
    self.classes = copy.copy(classes)
    self.writer = csv.writer(self.file, delimiter='\t')

  def preprocess(self, event):

    r = set()
    if isinstance(event, Call):
      #print event.name, event.param_types, event.ret, event.retaddr, event.retvalue
      (name, args) = event.GetTypedName()

      #r.add((name+":ret_addr",str(args[0])))
      r.add((name+":ret_val",str(args[1])))

      for (index, arg) in enumerate(args[2:]):
        r.add((name+":"+str(index),str(arg)))
        #print r
    elif isinstance(event, Abort):
      (name, fields) = event.GetTypedName()
      r.add((name+":eip",str(fields[0])))
    
    elif isinstance(event, Exit):
      (name, fields) = event.GetTypedName()
      r.add((name,str(())))
    
    elif isinstance(event, Crash):
      (name, fields) = event.GetTypedName()
      r.add((name+":eip",str(fields[0])))

    elif isinstance(event, Signal):
      #assert(0)
      (name, fields) = event.GetTypedName()

      if name == "SIGSEGV":
        #print fields[0]
        r.add((name+":addr",str(fields[0])))
      else:
        r.add((name,str(fields[0])))

    return r

  def set_original_events(self, events):
    r = list()

    for event in events:
      r = r + list(self.preprocess(event))
    
    self.original_events = r
    self.original_class = self.find_class(self.original_events)

  def find_class(self,events):

    for event in events:
      if event in self.classes:
        return self.classes[event]

    return self.classes['*']
 

  def print_events(self, delta, events):
     
    r = list()

    for event in events:
      r = r + list(self.preprocess(event))
    
    events = r

    x = hash(tuple(events))
    if (x in self.tests):
      return
 
    self.tests.add(x)

    # f(m, original_events) = new_class

    print self.pname+"\t"+str(delta)+"\t", 
    for x,y in self.original_events:
      print x+"="+y+" ",
      #assert(not ("abort" in str(x)))  

    print "\t"+str(self.find_class(events))+"\n",
   
    # f(-m, events) = old_class
    delta.inv()

    print self.pname+"\t"+str(delta)+"\t", 
    for x,y in events:
      print x+"="+y+" ",
      #assert(not ("abort" in str(x)))  

    print "\t"+str(self.original_class)+"\n",

    return
