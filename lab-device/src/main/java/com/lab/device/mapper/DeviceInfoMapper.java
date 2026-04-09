package com.lab.device.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.lab.device.entity.DeviceInfo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Update;

/**
 * 设备Mapper（含乐观锁库存扣减）
 */
@Mapper
public interface DeviceInfoMapper extends BaseMapper<DeviceInfo> {

    /**
     * 乐观锁扣减可用库存
     * UPDATE device_info SET available_quantity = available_quantity - #{quantity}, version = version + 1
     * WHERE id = #{id} AND version = #{version} AND available_quantity >= #{quantity}
     *
     * @return 影响行数（1=成功，0=库存不足或版本冲突）
     */
    @Update("UPDATE device_info SET available_quantity = available_quantity - #{quantity}, " +
            "version = version + 1, update_time = NOW() " +
            "WHERE id = #{id} AND version = #{version} AND available_quantity >= #{quantity}")
    int decreaseAvailableQuantity(@Param("id") Long id, @Param("quantity") Integer quantity, @Param("version") Integer version);

    /**
     * 乐观锁回加可用库存
     * UPDATE device_info SET available_quantity = available_quantity + #{quantity}, version = version + 1
     * WHERE id = #{id} AND version = #{version}
     */
    @Update("UPDATE device_info SET available_quantity = available_quantity + #{quantity}, " +
            "version = version + 1, update_time = NOW() " +
            "WHERE id = #{id} AND version = #{version}")
    int increaseAvailableQuantity(@Param("id") Long id, @Param("quantity") Integer quantity, @Param("version") Integer version);
}
