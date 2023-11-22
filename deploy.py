from azure.identity import DefaultAzureCredential

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.network import NetworkManagementClient

from azure.mgmt.compute import ComputeManagementClient



def create_or_update_resource_group():

    # Define your Azure subscription ID and resource group name

    subscription_id = "fac290d9-3cb9-4872-91af-fbdbec02c347"

    resource_group_name = "lab4"

    location = "westeurope"  



    # Create a DefaultAzureCredential

    credential = DefaultAzureCredential()



    # Create a ResourceManagementClient instance

    client = ResourceManagementClient(credential, subscription_id)



    # Define the resource group parameters

    parameters = {"location": location}



    # Create or update the resource group

    result = client.resource_groups.create_or_update(resource_group_name, parameters)

    print(f"Resource group creation/update status: {result}\n\n")



def create_virtual_network():

    client = NetworkManagementClient(

        credential=DefaultAzureCredential(),

        subscription_id="fac290d9-3cb9-4872-91af-fbdbec02c347",

    )



    response = client.virtual_networks.begin_create_or_update(

        resource_group_name="lab4",

        virtual_network_name="testNetwork",

        parameters={

            "location": "westeurope",

            "properties": {"addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}, "flowTimeoutInMinutes": 10},

        },

    ).result()

    print(f"Sucessfully created virtual network: {response}\n\n")



def create_subnet():

    client = NetworkManagementClient(

        credential=DefaultAzureCredential(),

        subscription_id="fac290d9-3cb9-4872-91af-fbdbec02c347",

    )



    response = client.subnets.begin_create_or_update(

        resource_group_name="lab4",

        virtual_network_name="testNetwork",

        subnet_name="testSubnet",

        subnet_parameters={"properties": {"addressPrefix": "10.0.0.0/16"}},

    ).result()

    print(f"Sucessfully created subnet {response}\n\n")



def create_public_ip_address():

    client = NetworkManagementClient(

        credential=DefaultAzureCredential(),

        subscription_id="fac290d9-3cb9-4872-91af-fbdbec02c347",

    )



    response = client.public_ip_addresses.begin_create_or_update(

        resource_group_name="lab4",

        public_ip_address_name="testIp",

        parameters={"location": "westeurope"},

    ).result()

    print(f"Sucessfully created IP address {response}\n\n")



def create_network_interface():

    client = NetworkManagementClient(

        credential=DefaultAzureCredential(),

        subscription_id="fac290d9-3cb9-4872-91af-fbdbec02c347",

    )



    try:

        response = client.network_interfaces.begin_create_or_update(

            resource_group_name="lab4",

            network_interface_name="testInterface",

            parameters={

                "location": "westeurope",

                "properties": {

                    #"disableTcpStateTracking": True,

                    "enableAcceleratedNetworking": True,

                    "ipConfigurations": [

                        {

                            "name": "test",

                            "properties": {

                                "publicIPAddress": {

                                    "id": "/subscriptions/fac290d9-3cb9-4872-91af-fbdbec02c347/resourceGroups/lab4/providers/Microsoft.Network/publicIPAddresses/testIp"

                                },

                                "subnet": {

                                    "id": "/subscriptions/fac290d9-3cb9-4872-91af-fbdbec02c347/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/testNetwork/subnets/testSubnet"

                                },

                            },

                        }

                    ],

                },

            },

        ).result()

        print(f"Sucessfully created network interface: {response}\n\n")

    except Exception as e:

        print(f"Error creating network interface: {e}")



def create_virtual_machine():

    # Define your Azure subscription ID and resource group name

    subscription_id = "298f8fe6-924c-4eaf-bbf6-eb25e12d5ead"

    resource_group_name = "lab4_test"

    location = "westeurope"  # Replace with the desired location



    # Create a DefaultAzureCredential

    credential = DefaultAzureCredential()



    # Create ComputeManagementClient and NetworkManagementClient instances

    compute_client = ComputeManagementClient(credential, subscription_id)

    network_client = NetworkManagementClient(credential, subscription_id)



    # Define VM configuration

    vm_name = "testVm"

    admin_username = "Hunny"

    ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDPNuUCd+m7Aoh6sMJ4siT3IeHdohtl5e9afJVWo/lsCKH9ma8xWedhOs0ICkznGsi2HGByq+D3vRMhxwN1qwCI9AytRBRelsMXeQP0+BarGnqtJ0e+UnUXGx36fYWYfPMYfHWPBF+hV+ZRNhYB2dCwQEs4Kd8jKAcZs/kylAt+8+g94/gXQ+W/6GM7oF3E+le2/5h5MmGs38zCW0XJhSXmd8TeelZ+k/4YFspe4rayeRMk+w/PiLhSVpXP49NIbnSY6MXZwGDZ6DBqQqqW3KHjx78v4CVWSG1tfOTgVgr3V1Bu4fytWfjYP3Du9a2lHfWI37mZWJ6oC5byH82jG+4oV+uvMqa/phHuuYMUdglyPivpvsRgvfLh+vileh0KdDh0/2RScqpc9HFuaGe90swD2DKxGdEt9wPdQCB3t4CVoRjafUikY4bcTUHcrruaMZvvp2H1vsJhzdCBT+7tivxHjN3fL3LljE2mkF0O3Xu84ROFEsL3m06zIOT+BuV+hMc="

    vm_size = "Standard_D1_v2"



    # Define the virtual machine properties

    vm_properties = {

        "location": location,

        "osProfile": {

            "adminUsername": admin_username,

            "secrets": [],

            "computerName": vm_name,

            "linuxConfiguration": {

                "ssh": {

                    "publicKeys": [

                        {

                            "path": "/home/fajaralbalushi/.ssh/authorized_keys",

                            "keyData": ssh_public_key

                        }

                    ]

                },

                "disablePasswordAuthentication": True

            }

        },

        "networkProfile": {

            "networkInterfaces": [

                {

                    "id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/testInterface",

                    "properties": {

                        "primary": True

                    }

                }

            ]

        },

        "storageProfile": {

            "imageReference": {

                "sku": "16.04-LTS",

                "publisher": "Canonical",

                "version": "latest",

                "offer": "UbuntuServer"

            },

            "dataDisks": []

        },

        "hardwareProfile": {

            "vmSize": vm_size

        },

        "provisioningState": "Creating"

    }



    # Create the virtual machine

    vm = compute_client.virtual_machines.begin_create_or_update(

        resource_group_name, vm_name, vm_properties)

    vm.wait()

    print("Successfully created VM!\n")

    print(vm.result())





if __name__ == "__main__":

    create_or_update_resource_group()

    create_virtual_network()

    create_subnet()

    create_public_ip_address()

    create_network_interface()

    create_virtual_machine()
