#!/usr/local/bin/perl 
#cleanup_lines.pl  -l adirname
use File::Find;
$opts = shift @ARGV;
if ($opts =~ /^-/) {
    ($args) = ($opts =~ /^-(.*)/);
    $dirname = shift @ARGV;
} else {
    $dirname = $opts;
}
print "args ",$args,"\n";
print "dirname $dirname \n";
$pwd=$ENV{'PWD'};
print "pwd $pwd\n";

find(\&wanted,$dirname);



sub wanted {
    if (
	($_ =~ /clean_channel.*/) |
	($_ =~ /channel.*/) |
	($_ =~ /list_channel.*/) |
	($_ =~ /mem_lS.*/) |
	($_ =~ /.*uvmem.*casa.*.log/) )
    {
	if ($args =~ /l/) {
	    print $File::Find::name,"\n";
	}
	if ($args =~ /k/) {
	    #print "Filename: $File::Find::name \n";
	    #unlink $File::Find::name or die "cannot unlink:$!";
	    print("rm -rf $File::Find::name\n");
	    system("rm -rf $File::Find::name");
	}
    }
}
 
