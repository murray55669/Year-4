import sys

if __name__ == '__main__':
  f = open(sys.argv[1])
  
  highest = 0
  
  for line in f:
    chunks = line.strip().split(' ')
    as_num = int(chunks[2])
    if as_num > highest:
      highest = as_num
    if len(bin(as_num))-2 >= 17:
      print 'long!'
      
  print highest