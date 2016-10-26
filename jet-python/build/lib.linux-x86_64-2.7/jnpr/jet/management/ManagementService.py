#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface:
  """
  Management APIs supported in JET
  """
  def LoginCheck(self, user, passwd):
    """
    Authenticate the user using this LoginCheck API.
    Returns boolean value indicating login successful or failed

    Parameters:
     - user: String representation of the username
     - passwd: String representation of the user's password
    """
    pass

  def ConfigureEphemeralSession(self, eph_config):
    """
    API to set ephemeral option, 0 on success and error code on failure.

    Parameters:
     - eph_config: Ephemeral configuration
    """
    pass

  def ExecuteOpCommand(self, op_command):
    """
        The argument op_command is a structure which can take JSON, CLI, XML as command inputs with filling
        appropriate fields in the structure. Examples can be referred from below.
        
        <pre>
         Example:
        op_command = OperationCommand("show interfaces em0", OperationFormatType.OPERATION_FORMAT_CLI,
                                                            OperationFormatType.OPERATION_FORMAT_CLI);
        result = mgmt_handle.ExecuteOpCommand(op_command)
        print 'Invoked ExecuteOpRpc \nreturn = ', result
        
        json_query = "{ \"get-interface-information\" : { \"interface-name\" : \"em0\" } }"
        op_command = OperationCommand(json_query,
                                                            OperationFormatType.OPERATION_FORMAT_JSON,
                                                            OperationFormatType.OPERATION_FORMAT_JSON);
        result = mgmt_handle.ExecuteOpCommand(op_command)
        print 'Invoked ExecuteOpRpc \nreturn = ', result
        
        xml_query = "&ltget-interface-information &gt &ltinterface-name&gtem0&lt/interface-name&gt &ltdetail/&gt &lt/get-interface-information&gt"
        op_command = OperationCommand(xml_query, in_format=OperationFormatType.OPERATION_FORMAT_XML,
                                                            out_format=OperationFormatType.OPERATION_FORMAT_XML);
        result = mgmt_handle.ExecuteOpCommand(op_command)
        print 'Invoked ExecuteOpRpc \nreturn = ', result
     
    <br>
    </pre>
         returns OperationResponse.status.err_code with 0 on success else nonzero value, response string will
         have appropriate output formatted string. <br><br>

         Note: The CLI command with pipe '|' option is not supported, hence the options included with '|' will be ignored
               in the processing. Example: "show interfaces terse ge-0/0/* | grep inet" is same as "show interfaces terse ge-0/0/*" both will
               return exactly the same information in the response.


    Parameters:
     - op_command: Command input
    """
    pass

  def ExecuteCfgCommand(self, config_commit):
    """
     Configurng and committing the configuration on the device.
     The configuration changes are made with exclusive mode if the configuration being made is on static DB.
     The possible configuration formats are text, set, xml and json. The default format will be json in future.
     Currently the formats supported are set, xml, text formats only.
     The database types also can be passed like shared, private, batch, ephemeral. The default database is
     shared and is the only database type supported now.
     
    <pre>
    Example:
      
     snmp_config = "
     		set snmp view readall oid .1 include
     		set snmp community test123 view readall
     		set snmp community test123 authorization read-write
     	"
     commit = ConfigCommit(ConfigCommitType.CONFIG_COMMIT, "Test comment", "")
     config = ConfigLoadCommit(snmp_config,ConfigFormatType.CONFIG_FORMAT_SET, ConfigDatabaseType.CONFIG_DB_SHARED,
     						  ConfigLoadType.CONFIG_LOAD_REPLACE, commit)
     result = mgmt_handle.ExecuteCfgCommand(config)
     print 'Invoked ExecuteCfgCommit \nreturn = ', result
     
     snmp_config = "
     	snmp {
     		view readall {
     			oid .1 include;
     		}
     
     		community test123 {
     			view readall;
     			authorization read-write;
     		}
     	}
     	"
     config = ConfigLoadCommit(snmp_config,ConfigFormatType.CONFIG_FORMAT_TEXT, ConfigDatabaseType.CONFIG_DB_SHARED,
     						  ConfigLoadType.CONFIG_LOAD_MERGE, commit)
     result = mgmt_handle.ExecuteCfgCommand(config)
     print 'Invoked ExecuteCfgCommit \nreturn = ', result
     
     snmp_config = "
     		&ltsnmp&gt
     			&ltview&gt
     				&ltname&gtreadall&lt/name&gt
     				&ltoid&gt
     					&ltname&gt.1&lt/name&gt
     					&ltinclude/&gt
     				&lt/oid&gt
     				&ltoid&gt
     					&ltname&gt.1.3&lt/name&gt
     					&ltexclude/&gt
     				&lt/oid&gt
     			&lt/view&gt
     			&ltcommunity&gt
     				&ltname&gttest123&lt/name&gt
     				&ltview&gtreadall&lt/view&gt
     				&ltauthorization&gtread-write&lt/authorization&gt
     			&lt/community&gt
     		&lt/snmp&gt
     	"
     config = ConfigLoadCommit(snmp_config,ConfigFormatType.CONFIG_FORMAT_XML, ConfigDatabaseType.CONFIG_DB_SHARED,
     						  ConfigLoadType.CONFIG_LOAD_REPLACE, commit)
     result = mgmt_handle.ExecuteCfgCommand(config)
     print 'Invoked ExecuteCfgCommit \nreturn = ', result

    </pre>
     
     returns RetStatus.err_code with 0 on success else nonzero value<br>

    Parameters:
     - config_commit: ConfigLoadCommit of type set, xml, text
    """
    pass


class Client(Iface):
  """
  Management APIs supported in JET
  """
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def LoginCheck(self, user, passwd):
    """
    Authenticate the user using this LoginCheck API.
    Returns boolean value indicating login successful or failed

    Parameters:
     - user: String representation of the username
     - passwd: String representation of the user's password
    """
    self.send_LoginCheck(user, passwd)
    return self.recv_LoginCheck()

  def send_LoginCheck(self, user, passwd):
    self._oprot.writeMessageBegin('LoginCheck', TMessageType.CALL, self._seqid)
    args = LoginCheck_args()
    args.user = user
    args.passwd = passwd
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_LoginCheck(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = LoginCheck_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "LoginCheck failed: unknown result");

  def ConfigureEphemeralSession(self, eph_config):
    """
    API to set ephemeral option, 0 on success and error code on failure.

    Parameters:
     - eph_config: Ephemeral configuration
    """
    self.send_ConfigureEphemeralSession(eph_config)
    return self.recv_ConfigureEphemeralSession()

  def send_ConfigureEphemeralSession(self, eph_config):
    self._oprot.writeMessageBegin('ConfigureEphemeralSession', TMessageType.CALL, self._seqid)
    args = ConfigureEphemeralSession_args()
    args.eph_config = eph_config
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_ConfigureEphemeralSession(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = ConfigureEphemeralSession_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "ConfigureEphemeralSession failed: unknown result");

  def ExecuteOpCommand(self, op_command):
    """
        The argument op_command is a structure which can take JSON, CLI, XML as command inputs with filling
        appropriate fields in the structure. Examples can be referred from below.
        
        <pre>
         Example:
        op_command = OperationCommand("show interfaces em0", OperationFormatType.OPERATION_FORMAT_CLI,
                                                            OperationFormatType.OPERATION_FORMAT_CLI);
        result = mgmt_handle.ExecuteOpCommand(op_command)
        print 'Invoked ExecuteOpRpc \nreturn = ', result
        
        json_query = "{ \"get-interface-information\" : { \"interface-name\" : \"em0\" } }"
        op_command = OperationCommand(json_query,
                                                            OperationFormatType.OPERATION_FORMAT_JSON,
                                                            OperationFormatType.OPERATION_FORMAT_JSON);
        result = mgmt_handle.ExecuteOpCommand(op_command)
        print 'Invoked ExecuteOpRpc \nreturn = ', result
        
        xml_query = "&ltget-interface-information &gt &ltinterface-name&gtem0&lt/interface-name&gt &ltdetail/&gt &lt/get-interface-information&gt"
        op_command = OperationCommand(xml_query, in_format=OperationFormatType.OPERATION_FORMAT_XML,
                                                            out_format=OperationFormatType.OPERATION_FORMAT_XML);
        result = mgmt_handle.ExecuteOpCommand(op_command)
        print 'Invoked ExecuteOpRpc \nreturn = ', result
     
    <br>
    </pre>
         returns OperationResponse.status.err_code with 0 on success else nonzero value, response string will
         have appropriate output formatted string. <br><br>

         Note: The CLI command with pipe '|' option is not supported, hence the options included with '|' will be ignored
               in the processing. Example: "show interfaces terse ge-0/0/* | grep inet" is same as "show interfaces terse ge-0/0/*" both will
               return exactly the same information in the response.


    Parameters:
     - op_command: Command input
    """
    self.send_ExecuteOpCommand(op_command)
    return self.recv_ExecuteOpCommand()

  def send_ExecuteOpCommand(self, op_command):
    self._oprot.writeMessageBegin('ExecuteOpCommand', TMessageType.CALL, self._seqid)
    args = ExecuteOpCommand_args()
    args.op_command = op_command
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_ExecuteOpCommand(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = ExecuteOpCommand_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "ExecuteOpCommand failed: unknown result");

  def ExecuteCfgCommand(self, config_commit):
    """
     Configurng and committing the configuration on the device.
     The configuration changes are made with exclusive mode if the configuration being made is on static DB.
     The possible configuration formats are text, set, xml and json. The default format will be json in future.
     Currently the formats supported are set, xml, text formats only.
     The database types also can be passed like shared, private, batch, ephemeral. The default database is
     shared and is the only database type supported now.
     
    <pre>
    Example:
      
     snmp_config = "
     		set snmp view readall oid .1 include
     		set snmp community test123 view readall
     		set snmp community test123 authorization read-write
     	"
     commit = ConfigCommit(ConfigCommitType.CONFIG_COMMIT, "Test comment", "")
     config = ConfigLoadCommit(snmp_config,ConfigFormatType.CONFIG_FORMAT_SET, ConfigDatabaseType.CONFIG_DB_SHARED,
     						  ConfigLoadType.CONFIG_LOAD_REPLACE, commit)
     result = mgmt_handle.ExecuteCfgCommand(config)
     print 'Invoked ExecuteCfgCommit \nreturn = ', result
     
     snmp_config = "
     	snmp {
     		view readall {
     			oid .1 include;
     		}
     
     		community test123 {
     			view readall;
     			authorization read-write;
     		}
     	}
     	"
     config = ConfigLoadCommit(snmp_config,ConfigFormatType.CONFIG_FORMAT_TEXT, ConfigDatabaseType.CONFIG_DB_SHARED,
     						  ConfigLoadType.CONFIG_LOAD_MERGE, commit)
     result = mgmt_handle.ExecuteCfgCommand(config)
     print 'Invoked ExecuteCfgCommit \nreturn = ', result
     
     snmp_config = "
     		&ltsnmp&gt
     			&ltview&gt
     				&ltname&gtreadall&lt/name&gt
     				&ltoid&gt
     					&ltname&gt.1&lt/name&gt
     					&ltinclude/&gt
     				&lt/oid&gt
     				&ltoid&gt
     					&ltname&gt.1.3&lt/name&gt
     					&ltexclude/&gt
     				&lt/oid&gt
     			&lt/view&gt
     			&ltcommunity&gt
     				&ltname&gttest123&lt/name&gt
     				&ltview&gtreadall&lt/view&gt
     				&ltauthorization&gtread-write&lt/authorization&gt
     			&lt/community&gt
     		&lt/snmp&gt
     	"
     config = ConfigLoadCommit(snmp_config,ConfigFormatType.CONFIG_FORMAT_XML, ConfigDatabaseType.CONFIG_DB_SHARED,
     						  ConfigLoadType.CONFIG_LOAD_REPLACE, commit)
     result = mgmt_handle.ExecuteCfgCommand(config)
     print 'Invoked ExecuteCfgCommit \nreturn = ', result

    </pre>
     
     returns RetStatus.err_code with 0 on success else nonzero value<br>

    Parameters:
     - config_commit: ConfigLoadCommit of type set, xml, text
    """
    self.send_ExecuteCfgCommand(config_commit)
    return self.recv_ExecuteCfgCommand()

  def send_ExecuteCfgCommand(self, config_commit):
    self._oprot.writeMessageBegin('ExecuteCfgCommand', TMessageType.CALL, self._seqid)
    args = ExecuteCfgCommand_args()
    args.config_commit = config_commit
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_ExecuteCfgCommand(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = ExecuteCfgCommand_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "ExecuteCfgCommand failed: unknown result");


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["LoginCheck"] = Processor.process_LoginCheck
    self._processMap["ConfigureEphemeralSession"] = Processor.process_ConfigureEphemeralSession
    self._processMap["ExecuteOpCommand"] = Processor.process_ExecuteOpCommand
    self._processMap["ExecuteCfgCommand"] = Processor.process_ExecuteCfgCommand

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_LoginCheck(self, seqid, iprot, oprot):
    args = LoginCheck_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = LoginCheck_result()
    result.success = self._handler.LoginCheck(args.user, args.passwd)
    oprot.writeMessageBegin("LoginCheck", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_ConfigureEphemeralSession(self, seqid, iprot, oprot):
    args = ConfigureEphemeralSession_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = ConfigureEphemeralSession_result()
    result.success = self._handler.ConfigureEphemeralSession(args.eph_config)
    oprot.writeMessageBegin("ConfigureEphemeralSession", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_ExecuteOpCommand(self, seqid, iprot, oprot):
    args = ExecuteOpCommand_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = ExecuteOpCommand_result()
    result.success = self._handler.ExecuteOpCommand(args.op_command)
    oprot.writeMessageBegin("ExecuteOpCommand", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_ExecuteCfgCommand(self, seqid, iprot, oprot):
    args = ExecuteCfgCommand_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = ExecuteCfgCommand_result()
    result.success = self._handler.ExecuteCfgCommand(args.config_commit)
    oprot.writeMessageBegin("ExecuteCfgCommand", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class LoginCheck_args:
  """
  Attributes:
   - user: String representation of the username
   - passwd: String representation of the user's password
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'user', None, None, ), # 1
    (2, TType.STRING, 'passwd', None, None, ), # 2
  )

  def __init__(self, user=None, passwd=None,):
    self.user = user
    self.passwd = passwd

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.user = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.passwd = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('LoginCheck_args')
    if self.user is not None:
      oprot.writeFieldBegin('user', TType.STRING, 1)
      oprot.writeString(self.user)
      oprot.writeFieldEnd()
    if self.passwd is not None:
      oprot.writeFieldBegin('passwd', TType.STRING, 2)
      oprot.writeString(self.passwd)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.user is None:
      raise TProtocol.TProtocolException(message='Required field user is unset!')
    if self.passwd is None:
      raise TProtocol.TProtocolException(message='Required field passwd is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class LoginCheck_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.BOOL, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.BOOL:
          self.success = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('LoginCheck_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.BOOL, 0)
      oprot.writeBool(self.success)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ConfigureEphemeralSession_args:
  """
  Attributes:
   - eph_config: Ephemeral configuration
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'eph_config', (EphemeralConfig, EphemeralConfig.thrift_spec), None, ), # 1
  )

  def __init__(self, eph_config=None,):
    self.eph_config = eph_config

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.eph_config = EphemeralConfig()
          self.eph_config.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ConfigureEphemeralSession_args')
    if self.eph_config is not None:
      oprot.writeFieldBegin('eph_config', TType.STRUCT, 1)
      self.eph_config.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ConfigureEphemeralSession_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRUCT, 'success', (jnpr.jet.shared.ttypes.RetStatus, jnpr.jet.shared.ttypes.RetStatus.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRUCT:
          self.success = jnpr.jet.shared.ttypes.RetStatus()
          self.success.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ConfigureEphemeralSession_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRUCT, 0)
      self.success.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ExecuteOpCommand_args:
  """
  Attributes:
   - op_command: Command input
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'op_command', (OperationCommand, OperationCommand.thrift_spec), None, ), # 1
  )

  def __init__(self, op_command=None,):
    self.op_command = op_command

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.op_command = OperationCommand()
          self.op_command.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ExecuteOpCommand_args')
    if self.op_command is not None:
      oprot.writeFieldBegin('op_command', TType.STRUCT, 1)
      self.op_command.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ExecuteOpCommand_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRUCT, 'success', (OperationResponse, OperationResponse.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRUCT:
          self.success = OperationResponse()
          self.success.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ExecuteOpCommand_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRUCT, 0)
      self.success.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ExecuteCfgCommand_args:
  """
  Attributes:
   - config_commit: ConfigLoadCommit of type set, xml, text
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'config_commit', (ConfigLoadCommit, ConfigLoadCommit.thrift_spec), None, ), # 1
  )

  def __init__(self, config_commit=None,):
    self.config_commit = config_commit

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.config_commit = ConfigLoadCommit()
          self.config_commit.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ExecuteCfgCommand_args')
    if self.config_commit is not None:
      oprot.writeFieldBegin('config_commit', TType.STRUCT, 1)
      self.config_commit.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ExecuteCfgCommand_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRUCT, 'success', (jnpr.jet.shared.ttypes.RetStatus, jnpr.jet.shared.ttypes.RetStatus.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRUCT:
          self.success = jnpr.jet.shared.ttypes.RetStatus()
          self.success.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ExecuteCfgCommand_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRUCT, 0)
      self.success.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
