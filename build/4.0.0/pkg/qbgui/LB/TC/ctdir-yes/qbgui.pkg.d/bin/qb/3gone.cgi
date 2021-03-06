#!/usr/bin/perl
use CGI;
use Data::Dumper;
require ("qbmod.cgi");

print "Content-type:text/html\n\n";

print qq(<html><head><link rel="stylesheet" href="gui.css" type="text/css"></head><body  bgcolor="#336699">);
print qq (<div align="center">);
print qq (<form name="info_3G_form" method="post" action="3gone.cgi">);

    runCommand(command=>'/usr/bin/killall ', params=>'-9 3ginfo_realtime.cgi');
    runCommand(command=>'/usr/bin/killall ', params=>'-9 3gtwo.cgi');
    runCommand(command=>'/usr/bin/killall ', params=>'-9 get3gsignal.sh');

    my $interface=$ENV{'QUERY_STRING'};
    $interface=~s/interface=//;
    
#    print qq ($interface,);
    print qq (<input type="hidden" id="interface_name" value=$interface>);
    my $Info_3G=XMLread($gACTIVEPATH."basic.xml");
    my $List_3G=$Info_3G->{isp};
    my %titleWidth=(Interface=>'40', IMEI=>'120', IP=>'120', Model=>'150', Signal=>'62', ISP=>'150', "Cell ID"=>'50', Band=>'70', RSSI=>'70', RSCP=>'70', ecio=>'70', Tx=>'70', Rx=>'70', Status=>'20' );
    my @titleList=('Interface', 'IMEI', 'IP', 'Model', 'Signal', "ISP", 'Cell ID', 'Band', 'RSSI', 'RSCP', 'Ec/Io', 'Tx', 'Rx', 'Status');

    print qq (<font class="bigtitle">3G Modem Information</font><hr size="1">);
    print qq (<table id="3ginfo" cellspacing="1" cellpadding="1" class="body" >);
    print qq (<tr bgcolor="#664422">);
    foreach my $title ( @titleList ) { print qq (<td class="body" width="$titleWidth{$title}" align="center">$title</td>); }
    print qq (</tr>);
    
    my $lineCount=1;

    foreach my $isp ( @$List_3G ) 
    {
        my $bgColor=($lineCount%2) ? ("#556677") : ("#334455");

        if ( $isp->{pppoeportdev} ne $interface || $isp->{flag_3g} ne "1" || $isp->{pppoeportdev} eq "" ) { next; }

	print qq (<tr bgcolor="$bgColor" originalColor="$bgColor" cellspacing="0" cellpadding="0" >);
	#===================================================================      
        my $pnum=$isp->{pppoeportdev}; $pnum=~s/ttyUSB//;
        my $display= ( $isp->{interface_name} && $isp->{imei} ) ? ($isp->{interface_name}) : (Modem .++$pnum);
        #my $display= Modem .++$pnum;
        print qq (<td class="body"  align="center"  width="$titleWidth{Interface}" title="$isp->{pppoeportdev}" >$display</td>);

        #===================================================================      
        my $usbdeviceinfo;
        my @usbdevicerecord;
        if (! open(DETECT_LOCK, "/tmp/detectusb.lock"))
        {
         $usbdeviceinfo=runCommand(command=>"cat", params=>'/tmp/usbdev.tab');
         @usbdevicerecord=split(/\n/, $usbdeviceinfo);
        }else{
         $usbdeviceinfo=runCommand(command=>"cat", params=>'/tmp/usbdev.tab.bak');
         @usbdevicerecord=split(/\n/, $usbdeviceinfo);
        }
        close(DETECT_LOCK);

#        print qq (<td class="body" align="center" width="$titleWidth{IMEI}">$isp->{imei}</td>);
#        print qq (<td class="body" align="center" width="$titleWidth{IP}">$isp->{systemip}</td>);

        my $display;
        foreach my $record ( @usbdevicerecord )
        {
            #print qq (<td>NIC:$record $isp->{pppoeportdev} </td>);
            if ( $isp->{interface_name} && $isp->{imei} )
            {
             if ( grep(/$isp->{imei} /, $record) )
             {
               my @imei=split(/ /, $record);
               my @modem=split(/Information:/, $record);
               print qq (<td class="body" align="center" width="$titleWidth{IMEI}">$imei[4]</td>);
               print qq (<td class="body" align="center" width="$titleWidth{IP}">$isp->{systemip}</td>);
               print qq (<td class="body" align="center" width="$titleWidth{Model}">$modem[1]</td>);
             }
            }
            else
            {
             if ( grep(/$isp->{pppoeportdev} /, $record) )
             {
               my @imei=split(/ /, $record);
               my @modem=split(/Information:/, $record);
	       print qq (<td class="body" align="center" width="$titleWidth{IMEI}">$imei[4]</td>);
               print qq (<td class="body" align="center" width="$titleWidth{IP}">$isp->{systemip}</td>);
               print qq (<td class="body" align="center" width="$titleWidth{Model}">$modem[1]</td>);
             }
            }
        }
        #=================================================================== 
#	my $signal=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} signal));
#        $signal=~s/\n//g;
#        if ( $signal eq "99" ){ $signal="0"; }
#        my $signalfree = 31 - $signal;
#        my $usage_3g=int $signal/31*100;
#        my $RSSI=113-($signal*2);
        print qq (<td class="body" width="62" align="center">);
        print qq (<span id="signal$isp->{pppoeportdev}" ><table width=100% border=0 cellpadding=0 cellspacing=0 >);
#        print qq (<td width="$signal" height="18" background="../image/usage.gif" title="signal strength : $usage_3g% RSSI:-$RSSI dBm">);
#        print qq (</td>);
#        print qq (<td width="$signalfree" height="18" background="../image/free.gif">);
#        print qq (</td>);
        print qq (</table></span>);
        print qq (</td>);
                                
        #===================================================================      
        my $isp_3G="";
        $isp_3G=~s/\n//g;
        if ( $isp_3G eq "0" ){ $isp_3G="None"; }
        print qq (<td class="body" align="center" width="$titleWidth{ISP}"><span id="isp3G$isp->{pppoeportdev}"> </span></td>);
        
        #===================================================================      
        # my $cell_id=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} cell));
        # if ( $cell_id eq "" ){ 
		$cell_id="None"; 
		# }
        print qq (<td class="body" align="center" width="$titleWidth{'Cell ID'}"><span id="cell$isp->{pppoeportdev}">$cell_id</span></td>);

        #===================================================================      
        my $band=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} band));
        if ( $band eq "" ){ $band="None"; }
        print qq (<td class="body" align="center" width="$titleWidth{Band}"><span id="band$isp->{pppoeportdev}">WCDMA</span></td>);

        #===================================================================      

        print qq (<td class="body" align="center" width="$titleWidth{RSSI}"><span id="RSSI$isp->{pppoeportdev}"> dBm</span></td>);
        print qq (<td class="body" align="center" width="$titleWidth{RSCP}"><span id="RSCP$isp->{pppoeportdev}"> </span></td>);
        print qq (<td class="body" align="center" width="$titleWidth{ecio}"><span id="ecio$isp->{pppoeportdev}"> </span></td>);

        #===================================================================      

        #===================================================================      
#        my $tx=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} tx));
        print qq (<td class="body" align="center" width="$titleWidth{Tx}"><span id="tx$isp->{pppoeportdev}"> kbps</span></td>);

        #===================================================================      
#        my $rx=runCommand(command=>'/opt/qb/hsdpa/get3gsignal.sh', params=>qq($isp->{pppoeportdev} rx));
        print qq (<td class="body" align="center" width="$titleWidth{Rx}"><span id="rx$isp->{pppoeportdev}"> kbps</span></td>);

        #===================================================================      
        my $imgsrc = ( $isp->{alive} ) ? ( 'alive.png' ) : ( 'dead.png' );
        print qq (<td class="body" align="center" width="$titleWidth{Status}"><span id="img$isp->{pppoeportdev}"><img src="image/$imgsrc" width="14" height="14" border="0" /></span></td>);
        print qq (</td>);
	
        $lineCount++;
    }

print qq (<tr><td colspan="8"><hr size="1"></td></tr>);
	print qq (</tr><td align="right" valign="top">);
	print qq (<input type="button" class="qb" name="watchAll" value="View all" title="Show all 3G information" style="width:70" onClick="watchall()" >); 
        print qq (</td>);
print qq (<tr><td colspan="8" align="left" class="body">);
print qq (</td></tr>);
print qq (</tr>);
print qq (</table>);
print qq (</form>);
print qq (</div>);
print qq(</body></html> );

#=================================================================== 
    print << "ISPSCRIPT";
    <script type="text/javascript" src="grid.js"></script>
    <script language="javascript">
   
    var myform;
    var queryReqHandler ;
    var interface_name=document.getElementById("interface_name").value;
    var select=0;
    var pre_status=new Array("signal","ecio","tx","isp","rx","band","cell");
    function ajax()
    {
    	if(select > pre_status.length-1){ select=0;}
        var i=(new Date()).getTime();
        var a=0;
		if (window.XMLHttpRequest)
	  {// code for all new browsers
	  queryReqHandler=new XMLHttpRequest();
	  }
	else if (window.ActiveXObject)
	  {// code for IE5 and IE6
	  queryReqHandler=new ActiveXObject("Microsoft.XMLHTTP");
	  }
	
//	if(queryReqHandler){ alert('queryReqHandler_OK'); }
	queryReqHandler.onreadystatechange = fno;
	queryReqHandler.open("GET","3gtwo.cgi?interface="+interface_name+"&a="+i+"&action="+pre_status[select],true);
	queryReqHandler.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	var str='';
	queryReqHandler.send(str);
	select++;
  
    }

    function fno()
    {
	if( (queryReqHandler.readyState == 4) && (queryReqHandler.status == 200) )
	{
	    var msg=queryReqHandler.responseText;
	    msg=msg.slice(0,msg.length-1);
	    //alert(msg);
	    msg=msg.split(",");
//	    var n=0;
	    if ( msg[0] == "alive" )
	    {
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[2]+"' width='14 height='14' border='0' />";
	    }
	    if ( msg[0] == "signal" )
	    {
	       	    document.getElementById("signal"+msg[1]).innerHTML="<table width='100%' border='0' cellpadding='0' cellspacing='0' ><td width='"+msg[2]+"' height='18' background='../image/usage.gif' title='signal strengtn : "+msg[4]+"% RSSI:-"+msg[5]+" dBm'></td>"+
        		"<td width="+msg[3]+" height='18' background='../image/free.gif'></td></table>";
       	    document.getElementById("RSSI"+msg[1]).innerHTML="-"+msg[5]+" dbm";
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[6]+"' width='14 height='14' border='0' />";
	    }
	    if ( msg[0] == "tx" || msg[0] == "rx" )
	    {
		    document.getElementById("tx"+msg[1]).innerHTML=msg[2]+"kbps";
		    document.getElementById("rx"+msg[1]).innerHTML=msg[3]+"kbps";
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[4]+"' width='14 height='14' border='0' />";
	    }
	    if ( msg[0] == "isp" )
	    {
	     	    document.getElementById("isp3G"+msg[1]).innerHTML=msg[2];
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[3]+"' width='14 height='14' border='0' />";
	    }
	    if ( msg[0] == "cell" )
	    {
	       	    document.getElementById("cell"+msg[1]).innerHTML=msg[2];
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[3]+"' width='14 height='14' border='0' />";
	    }
	    if ( msg[0] == "band" )
	    {
			if(msg[2] != "None"){
	       	document.getElementById("band"+msg[1]).innerHTML=msg[2];
			}
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[3]+"' width='14 height='14' border='0' />";
	    }
	    if ( msg[0] == "ecio" || msg[0] == "rscp" )
	    {
       	            document.getElementById("ecio"+msg[1]).innerHTML=msg[2];
          	    document.getElementById("RSCP"+msg[1]).innerHTML=msg[3];
		    document.getElementById("img"+msg[1]).innerHTML="<img src='image/"+msg[4]+"' width='14 height='14' border='0' />";
       	    }
       	    
//#     	    document.getElementById("isp3G"+msg[n+13]).innerHTML=msg[n+4];
//#       	    document.getElementById("cell"+msg[n+13]).innerHTML=msg[n+5];
//#       	    document.getElementById("band"+msg[n+13]).innerHTML=msg[n+6];
//       	    document.getElementById("RSSI"+msg[n+13]).innerHTML="-"+msg[n+7]+" dbm";
//       	    document.getElementById("RSCP"+msg[n+13]).innerHTML="-"+msg[n+9]+" dbm";
//       	    document.getElementById("ecio"+msg[n+13]).innerHTML="-"+msg[n+8]+" db";
//       	    document.getElementById("tx"+msg[n+13]).innerHTML=msg[n+10]+"kbps";
//       	    document.getElementById("rx"+msg[n+13]).innerHTML=msg[n+11]+"kbps";
//       	    document.getElementById("img"+msg[n+13]).innerHTML="<img src='image/"+msg[n+12]+"' width='14 height='14' border='0' />";
//       	    document.getElementById("signal"+msg[n+13]).innerHTML="<table width='100%' border='0' cellpadding='0' cellspacing='0' ><td width='"+msg[n]+"' height='18' background='../image/usage.gif' title='signal strengtn : "+msg[n+2]+"% RSSI:-"+msg[n+3]+" dBm'></td>"+
//        		"<td width="+msg[n+1]+" height='18' background='../image/free.gif'></td></table>";
	    queryReqHandler = null;
	    //ajax();
        setTimeout( "ajax()",5000 );
	}
    }
    function watchall()
    {
//        location.href="3ginfo.cgi?a="+(new Date()).getTime();
        location.href="3ginfo.cgi";
    }
    
    function cgi_dep_onload() { myform=window.document.forms[0]; }
    ajax();
    
    </script>
ISPSCRIPT
