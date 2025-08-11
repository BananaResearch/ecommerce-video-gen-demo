set -ex

imagetag=1.14
docker build -t ecommerce-video-gen:$imagetag .
docker tag ecommerce-video-gen:$imagetag baresearch-registry.cn-beijing.cr.aliyuncs.com/baresearch/ecommerce-video-gen:$imagetag
docker push baresearch-registry.cn-beijing.cr.aliyuncs.com/baresearch/ecommerce-video-gen:$imagetag