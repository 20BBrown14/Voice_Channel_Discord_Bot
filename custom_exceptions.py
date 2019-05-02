# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class zipcode_invalid_exception(Error):
  """Raised when a zipcode is used that is invalid"""
  pass