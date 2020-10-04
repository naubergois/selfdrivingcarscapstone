// Generated by gencpp from file dbw_mkz_msgs/TurnSignal.msg
// DO NOT EDIT!


#ifndef DBW_MKZ_MSGS_MESSAGE_TURNSIGNAL_H
#define DBW_MKZ_MSGS_MESSAGE_TURNSIGNAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace dbw_mkz_msgs
{
template <class ContainerAllocator>
struct TurnSignal_
{
  typedef TurnSignal_<ContainerAllocator> Type;

  TurnSignal_()
    : value(0)  {
    }
  TurnSignal_(const ContainerAllocator& _alloc)
    : value(0)  {
  (void)_alloc;
    }



   typedef uint8_t _value_type;
  _value_type value;



  enum {
    NONE = 0u,
    LEFT = 1u,
    RIGHT = 2u,
  };


  typedef boost::shared_ptr< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> const> ConstPtr;

}; // struct TurnSignal_

typedef ::dbw_mkz_msgs::TurnSignal_<std::allocator<void> > TurnSignal;

typedef boost::shared_ptr< ::dbw_mkz_msgs::TurnSignal > TurnSignalPtr;
typedef boost::shared_ptr< ::dbw_mkz_msgs::TurnSignal const> TurnSignalConstPtr;

// constants requiring out of line definition

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace dbw_mkz_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'dbw_mkz_msgs': ['/home/nauber/CarND-Capstone/ros/src/dbw_mkz_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "52e47837caa6386d671c442331ecc1cd";
  }

  static const char* value(const ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x52e47837caa6386dULL;
  static const uint64_t static_value2 = 0x671c442331ecc1cdULL;
};

template<class ContainerAllocator>
struct DataType< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dbw_mkz_msgs/TurnSignal";
  }

  static const char* value(const ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 value\n\
\n\
uint8 NONE=0\n\
uint8 LEFT=1\n\
uint8 RIGHT=2\n\
";
  }

  static const char* value(const ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.value);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct TurnSignal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::dbw_mkz_msgs::TurnSignal_<ContainerAllocator>& v)
  {
    s << indent << "value: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.value);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DBW_MKZ_MSGS_MESSAGE_TURNSIGNAL_H
