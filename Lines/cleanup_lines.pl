#!/usr/bin/perl
#cleanup_lines.pl  -l adirname  list only
#cleanup_lines.pl  -k adirname  remove 
use File::Find;
use File::Path; #  qw(rmtree);
#use File::Basename;
# https://perldoc.perl.org/File::Find#The-wanted-function
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
if (!($dirname =~ /^\//)) {
    $dirname = $pwd."\/".$dirname;
}
print "dirname $dirname\n";


find(\&wanted,$dirname);



sub wanted {
    # $File::Find::dir is the current directory name,
    # $_ is the current filename within that directory
    # $File::Find::name is the complete pathname to the file.
    #$zbasename= basename($zname);
    $zbasename= $_;
    $zname = $File::Find::name;
    
    if (
	($zbasename =~ /clean_channel.*/) |
	($zbasename =~ /channel.*/) |
	($zbasename =~ /list_channel.*/) |
	($zname =~ /mem_lS.*/) |
	($zbasename =~ /^casa.*log/) )
    {
	if ($args =~ /l/) {
	    print $zname,"\n";
	    #print basename($File::Find::name),"\n";
	}
	elsif ($args =~ /k/) {
	    #print "Filename: $File::Find::name \n";
	    print("rm -rf $zname\n");

	    if (-d $zname) {
		print("directory ",$zname,"\n");
		&File::Path::rmtree($zname);
	    } else {
		unlink $zname or die "cannot unlink:$!";
	    }
	    #system("rm -rf $zname");
	}
    }
}
 
