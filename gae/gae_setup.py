import os
import sys
import google  # provided by GAE

# add vendorized protobuf to google namespace package
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
google.__path__.append(os.path.join(vendor_dir, 'google'))

# add stock libraries path
#trading_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#google.__path__.append(trading_dir)

# add paths
sys.path.insert(0, vendor_dir)
#sys.path.insert(0, trading_dir)
