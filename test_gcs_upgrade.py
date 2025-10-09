#!/usr/bin/env python3
"""
Test script to verify google-cloud-storage 2.3.0 compatibility
"""

import sys
import os

# Add the kserve package to the path
sys.path.insert(0, 'python/kserve')

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from google.cloud import storage
        from google.auth import exceptions
        print("✓ Successfully imported google.cloud.storage")
        print(f"  Version: {storage.__version__ if hasattr(storage, '__version__') else 'unknown'}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

def test_client_creation():
    """Test creating storage clients"""
    print("\nTesting client creation...")
    try:
        from google.cloud import storage
        from google.auth import exceptions
        
        # Test 1: Check if create_anonymous_client exists
        if hasattr(storage.Client, 'create_anonymous_client'):
            print("✓ create_anonymous_client method exists")
        else:
            print("✗ create_anonymous_client method NOT FOUND")
            return False
        
        # Test 2: Try to create an anonymous client
        try:
            client = storage.Client.create_anonymous_client()
            print("✓ Successfully created anonymous client")
        except Exception as e:
            print(f"✗ Failed to create anonymous client: {e}")
            return False
        
        # Test 3: Check bucket method
        if hasattr(client, 'bucket'):
            print("✓ bucket() method exists")
        else:
            print("✗ bucket() method NOT FOUND")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_kserve_storage():
    """Test that kserve.Storage can be imported"""
    print("\nTesting kserve.Storage...")
    try:
        import kserve
        if hasattr(kserve, 'Storage'):
            print("✓ kserve.Storage class exists")
            if hasattr(kserve.Storage, '_download_gcs'):
                print("✓ _download_gcs method exists")
            return True
        else:
            print("✗ kserve.Storage class NOT FOUND")
            return False
    except ImportError as e:
        print(f"✗ Failed to import kserve: {e}")
        return False

def main():
    print("=" * 60)
    print("Google Cloud Storage 2.3.0 Compatibility Test")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    
    if results[-1][1]:  # Only run if imports succeeded
        results.append(("Client Creation", test_client_creation()))
        results.append(("KServe Storage", test_kserve_storage()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! The upgrade should be compatible.")
    else:
        print("✗ Some tests failed. Review the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

