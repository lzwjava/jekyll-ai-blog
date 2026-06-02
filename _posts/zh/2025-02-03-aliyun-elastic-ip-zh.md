---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 阿里云弹性IP管理
translated: true
type: post
---

该脚本提供了一个命令行界面来管理阿里云弹性公网IP (EIP)。它允许你使用阿里云Python SDK创建、绑定、解绑和释放EIP。脚本接受要执行的任务和EIP的分配ID作为参数。

```bash
python aliyun_elastic_ip_manager.py unbind --allocation_id eip-j6c2olvsa7jk9l42iaaa
python aliyun_elastic_ip_manager.py bind --allocation_id eip-j6c7mhenamvy6zao3haaa
python aliyun_elastic_ip_manager.py release --allocation_id eip-j6c2olvsa7jk9l42aaa
python aliyun_elastic_ip_manager.py describe
```

```python
# -*- coding: utf-8 -*-
# 此文件是自动生成的，请勿编辑。谢谢。
import logging
import os
import sys
from typing import List
import argparse
import json

from alibabacloud_vpc20160428.client import Client as Vpc20160428Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_vpc20160428 import models as vpc_20160428_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Vpc20160428Client:
        config = open_api_models.Config(
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_ID_API_KEY'],
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_API_KEY']
        )
        config.endpoint = f'vpc.cn-hongkong.aliyuncs.com'
        return Vpc20160428Client(config)

    @staticmethod
    def bind_eip(
        region_id: str,
        allocation_id: str,
        instance_id: str,
    ) -> bool:
        client = Sample.create_client()
        associate_eip_address_request = vpc_20160428_models.AssociateEipAddressRequest(
            region_id=region_id,
            allocation_id=allocation_id,
            instance_id=instance_id
        )
        runtime = util_models.RuntimeOptions(read_timeout=60000, connect_timeout=60000)
        try:
            result = client.associate_eip_address_with_options(associate_eip_address_request, runtime)
            logging.info(f"已成功将EIP {allocation_id}绑定到实例 {instance_id}。结果：{result}")
            return True
        except Exception as error:
            logging.error(f"绑定EIP {allocation_id}到实例 {instance_id}时出错：{error}")
            if hasattr(error, 'message'):
                logging.error(f"错误信息：{error.message}")
            if hasattr(error, 'data') and error.data and error.data.get('Recommend'):
                logging.error(f"建议：{error.data.get('Recommend')}")
            UtilClient.assert_as_string(str(error))
            return False

    @staticmethod
    def unbind_eip(
        region_id: str,
        allocation_id: str,
        instance_id: str,
    ) -> bool:
        client = Sample.create_client()
        unassociate_eip_address_request = vpc_20160428_models.UnassociateEipAddressRequest(
            region_id=region_id,
            allocation_id=allocation_id,
            instance_id=instance_id
        )
        runtime = util_models.RuntimeOptions(read_timeout=60000, connect_timeout=60000)
        try:
            result = client.unassociate_eip_address_with_options(unassociate_eip_address_request, runtime)
            logging.info(f"已成功解除EIP {allocation_id}与实例 {instance_id} 的绑定。结果：{result}")
            return True
        except Exception as error:
            logging.error(f"解除EIP {allocation_id}与实例 {instance_id} 的绑定时出错：{error}")
            if hasattr(error, 'message'):
                logging.error(f"错误信息：{error.message}")
            if hasattr(error, 'data') and error.data and error.data.get('Recommend'):
                logging.error(f"建议：{error.data.get('Recommend')}")
            UtilClient.assert_as_string(str(error))
            return False

    @staticmethod
    def create_eip(
        region_id: str,
    ) -> str | None:
        client = Sample.create_client()
        allocate_eip_address_request = vpc_20160428_models.AllocateEipAddressRequest(
            region_id= region_id,
            instance_charge_type='PostPaid',
            internet_charge_type='PayByTraffic',
            bandwidth='200'
        )
        runtime = util_models.RuntimeOptions(read_timeout=60000, connect_timeout=60000)
        try:
            result = client.allocate_eip_address_with_options(allocate_eip_address_request, runtime)
            print(result.body)
            allocation_id = result.body.allocation_id
            logging.info(f"已成功创建EIP。分配ID：{allocation_id}")
            return allocation_id
        except Exception as error:
            logging.error(f"创建EIP时出错：{error}")
            if hasattr(error, 'message'):
                logging.error(f"错误信息：{error.message}")
            if hasattr(error, 'data') and error.data and error.data.get('Recommend'):
                logging.error(f"建议：{error.data.get('Recommend')}")
            UtilClient.assert_as_string(str(error))
            return None

    @staticmethod
    def release_eip(
        allocation_id: str,
    ) -> bool:
        client = Sample.create_client()
        release_eip_address_request = vpc_20160428_models.ReleaseEipAddressRequest(
            allocation_id=allocation_id
        )
        runtime = util_models.RuntimeOptions(read_timeout=60000, connect_timeout=60000)
        try:
            result = client.release_eip_address_with_options(release_eip_address_request, runtime)
            logging.info(f"已成功释放EIP {allocation_id}。结果：{result}")
            return True
        except Exception as error:
            logging.error(f"释放EIP {allocation_id}时出错：{error}")
            if hasattr(error, 'message'):
                logging.error(f"错误信息：{error.message}")
            if hasattr(error, 'data') and error.data and error.data.get('Recommend'):
                logging.error(f"建议：{error.data.get('Recommend')}")
            UtilClient.assert_as_string(str(error))
            return False

    @staticmethod
    def describe_eip(
        region_id: str,
        instance_id: str,
    ) -> str | None:
        client = Sample.create_client()
        describe_eip_addresses_request = vpc_20160428_models.DescribeEipAddressesRequest(
            region_id=region_id
        )
        runtime = util_models.RuntimeOptions(read_timeout=60000, connect_timeout=60000)
        try:
            result = client.describe_eip_addresses_with_options(describe_eip_addresses_request, runtime)
            logging.info(f"已成功描述EIP。")
            print(json.dumps(result.body.to_map(), indent=4))
            if result.body.eip_addresses and hasattr(result.body.eip_addresses, 'eip_address') and result.body.eip_addresses.eip_address:
                for eip in result.body.eip_addresses.eip_address:
                    if eip.instance_id == instance_id:
                        return eip.allocation_id
                logging.info(f"未找到实例 {instance_id} 的EIP地址")
                return None
            else:
                logging.info("未找到EIP地址。")
                return None
        except Exception as error:
            logging.error(f"描述EIP时出错：{error}")
            if hasattr(error, 'message'):
                logging.error(f"错误信息：{error.message}")
            if hasattr(error, 'data') and error.data and error.data.get('Recommend'):
                logging.error(f"建议：{error.data.get('Recommend')}")
            UtilClient.assert_as_string(str(error))
            return None

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        region_id = "cn-hongkong"
        instance_id = "i-j6c44l4zpphv7u7agdbk"

        parser = argparse.ArgumentParser(description='管理阿里云弹性公网IP。')
        parser.add_argument('job', choices=['create', 'bind', 'unbind', 'release', 'describe', 'all'], help='要执行的任务：创建、绑定或解绑。')
        parser.add_argument('--allocation_id', type=str, help='EIP的分配ID。')
        parser.add_argument('--instance_id', type=str, default=instance_id, help='要绑定/解绑EIP的实例ID。')

        parsed_args = parser.parse_args(args)

        if parsed_args.job == 'create':
            new_allocation_id = Sample.create_eip(region_id)
            if new_allocation_id:
                print(f"EIP创建过程已成功启动。分配ID：{new_allocation_id}")
            else:
                print("EIP创建过程失败。")
        elif parsed_args.job == 'bind':
            if not parsed_args.allocation_id:
                print("错误：bind 任务需要 --allocation_id 参数。")
                return
            if Sample.bind_eip(region_id, parsed_args.allocation_id, parsed_args.instance_id):
                print(f"EIP绑定过程已成功启动，EIP：{parsed_args.allocation_id}，实例：{parsed_args.instance_id}。")
            else:
                print(f"EIP绑定过程失败，EIP：{parsed_args.allocation_id}，实例：{parsed_args.instance_id}。")
        elif parsed_args.job == 'unbind':
            if not parsed_args.allocation_id:
                print("错误：unbind 任务需要 --allocation_id 参数。")
                return
            if Sample.unbind_eip(region_id, parsed_args.allocation_id, parsed_args.instance_id):
                print(f"EIP解绑过程已成功启动，EIP：{parsed_args.allocation_id}，实例：{parsed_args.instance_id}。")
            else:
                print(f"EIP解绑过程失败，EIP：{parsed_args.allocation_id}，实例：{parsed_args.instance_id}。")
        elif parsed_args.job == 'release':
            if not parsed_args.allocation_id:
                print("错误：release 任务需要 --allocation_id 参数。")
                return
            if Sample.release_eip(parsed_args.allocation_id):
                 print(f"EIP释放过程已成功启动，EIP：{parsed_args.allocation_id}。")
            else:
                print(f"EIP释放过程失败，EIP：{parsed_args.allocation_id}。")
        elif parsed_args.job == 'describe':
            if not parsed_args.instance_id:
                print("错误：describe 任务需要 --instance_id 参数。")
                return
            allocation_id = Sample.describe_eip(region_id, parsed_args.instance_id)
            if allocation_id:
                print(f"分配ID：{allocation_id}")
            else:
                print("未找到EIP。")
        elif parsed_args.job == 'all':
            # 查询以获取当前分配ID
            current_allocation_id = Sample.describe_eip(region_id, parsed_args.instance_id)
            if current_allocation_id:
                print(f"当前分配ID：{current_allocation_id}")
            else:
                print("未找到可处理的EIP。")
                return

            # 解绑当前EIP
            if current_allocation_id:
                if Sample.unbind_eip(region_id, current_allocation_id, parsed_args.instance_id):
                    print(f"已成功解除EIP {current_allocation_id}与实例 {parsed_args.instance_id} 的绑定。")
                else:
                    print(f"解除EIP {current_allocation_id}与实例 {parsed_args.instance_id} 的绑定失败。")
                    return

            # 创建新的EIP
            new_allocation_id = Sample.create_eip(region_id)
            if new_allocation_id:
                print(f"EIP创建过程已成功启动。新的分配ID：{new_allocation_id}")
            else:
                print("EIP创建过程失败。")
                return

            # 绑定新的EIP
            if Sample.bind_eip(region_id, new_allocation_id, parsed_args.instance_id):
                print(f"已成功将新的EIP {new_allocation_id}绑定到实例 {parsed_args.instance_id}。")
            else:
                print(f"将新的EIP {new_allocation_id}绑定到实例 {parsed_args.instance_id}失败。")
                return

            # 释放旧的EIP
            if current_allocation_id:
                if Sample.release_eip(current_allocation_id):
                    print(f"已成功释放旧的EIP {current_allocation_id}。")
                else:
                    print(f"释放旧的EIP {current_allocation_id}失败。")

            # 再次查询以显示最终状态
            final_allocation_id = Sample.describe_eip(region_id, parsed_args.instance_id)
            if final_allocation_id:
                print(f"最终分配ID：{final_allocation_id}")
            else:
                print("处理后未找到EIP。")


    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        associate_eip_address_request = vpc_20160428_models.AssociateEipAddressRequest(
            region_id='cn-hongkong'
        )
        runtime = util_models.RuntimeOptions()
        try:
            await client.associate_eip_address_with_options_async(associate_eip_address_request, runtime)
        except Exception as error:
            print(error)
            if hasattr(error, 'message'):
                print(error.message)
            if hasattr(error, 'data') and error.data.get("Recommend"):
                print(error.data.get("Recommend"))
            UtilClient.assert_as_string(str(error))


if __name__ == '__main__':
    Sample.main(sys.argv[1:])

# python scripts/auto-ss-config/aliyun_elastic_ip_manager.py create
# python scripts/auto-ss-config/aliyun_elastic_ip_manager.py unbind --allocation_id eip-j6c2olvsa7jk9l42i1aaa
# python scripts/auto-ss-config/aliyun_elastic_ip_manager.py bind --allocation_id eip-j6c7mhenamvy6zao3haaa
# python scripts/auto-ss-config/aliyun_elastic_ip_manager.py release --allocation_id "eip-j6c2olvsa7jk9l42i"
# python scripts/auto-ss-config/aliyun_elastic_ip_manager.py describe
# python scripts/auto-ss-config/aliyun_elastic_ip_manager.py all
```
