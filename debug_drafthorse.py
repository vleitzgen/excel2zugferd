from drafthorse.models.payment import PaymentMeans
from drafthorse.models.container import StringContainer
from drafthorse.models.elements import StringElement

try:
    pm = PaymentMeans()
    print(f"Type of pm.information: {type(pm.information)}")
    print(f"Is instance of StringContainer: {isinstance(pm.information, StringContainer)}")
    print(f"Is instance of StringElement: {isinstance(pm.information, StringElement)}")
    
    if hasattr(pm.information, 'add'):
        print("pm.information has 'add' method")
        pm.information.add("Test")
        print("Added 'Test' successfully")
    else:
        print("pm.information DOES NOT have 'add' method")

except Exception as e:
    print(f"Error: {e}")
