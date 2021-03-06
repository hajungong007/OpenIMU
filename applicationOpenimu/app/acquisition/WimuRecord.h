#ifndef WIMURECORD_H
#define WIMURECORD_H

#include <string>
#include "IJsonSerializable.h"
#include <vector>
#include "RecordInfo.h"

class WimuRecord : public IJsonSerializable
{
public:
   WimuRecord();
   virtual ~WimuRecord(void);

   virtual void Serialize( Json::Value& root, RecordInfo recordInfo, std::string& output);
   virtual void Deserialize( Json::Value& root);

   std::vector<RecordInfo> m_WimuRecordList;
};
#endif
