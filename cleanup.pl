#!/usr/local/bin/perl 
#cleanup_lines.pl  -l adirname
#belka16:19:26~$perl ~/gitcommon/GUVMEMscripts/cleanup.pl -lk ./


use File::Find;
use File::Spec;
use File::Path;
use File::Basename;
$opts = shift @ARGV;
if ($opts =~ /^-/) {
    ($args) = ($opts =~ /^-(.*)/);
    $dirname = shift @ARGV;
} else {
    $dirname = $opts;
}
print "args ",$args,"\n";
print "dirname $dirname \n";
if (! File::Spec->file_name_is_absolute($dirname)) {
    $dirname = File::Spec->rel2abs($dirname);
    print "converted to absolute path $dirname \n";
}
finddepth(\&wanted,$dirname);



sub wanted {
    $abasename = basename($File::Find::name);
    $adirname = basename($File::Find::name);
    $fullfilename=$File::Find::name;
    #if (-d) {
    #	print "$_ : this is a directory \n";
    #} else {
    #	
    #}
    if (
	($abasename =~ /^clean_channel.*/) |
	($abasename =~ /^channel.*\.ms$/) |
	($abasename =~ /^list_channel.*/) |
	($abasename =~ /^mem_lS.*chan\d+$/) |
	($fullfilename =~ /.*uvmem.*casa.*.log$/) )
    {
	if ($args =~ /l/) {
	    print $fullfilename,"\n";
	}
	if ($args =~ /k/) {
	    #print "Filename: $File::Find::name \n";
	    rmtree $fullfilename or warn "cannot rmtree:$!";

	    #if (!-l && -d _) {
	    #	print "rmdir $name\n";
	    #	rmdir($_)  or warn "couldn't rmdir $name: $!";
	    #} else {
	    #	print "unlink $name";
	    #	unlink($_) or warn "couldn't unlink $name: $!";
	    #}
	    #print("rm -rf $File::Find::name\n");
	    #system("rm -rf $File::Find::name");
	}
    }
}
 
