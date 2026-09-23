import math

frame = absTime.frame

# Move left and right
x = math.sin(frame * 0.03) * 2

# Move up and down
y = math.cos(frame * 0.03) * 1

# Control the Transform TOP/SOP
op('transform1').par.tx = x
op('transform1').par.ty = y