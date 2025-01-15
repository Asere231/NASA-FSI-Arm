import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/asere/NASA-FSI-Arm/arm_ws/install/arm_control'
