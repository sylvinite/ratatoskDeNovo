#!/usr/bin/perl -w

#
# Script to sync matefiles for PE alignment using Illumina data
# Agilent Technologies
#
# Modified 20130428 by Per Unneberg. 
# 
# The first implementation hashed
# the entire input sequence files, causing the program to crash when
# working on large input files. The new "-a" option uses the first
# implementation, "-b" only hashes the ids and re-read the sequence
# files when outputting the synced reads, and finally, the default is
# to read the files sequentially and output reads one by one, thus
# eliminating the need to load anything into memory
#

use strict;
use warnings;
use Getopt::Long;
use FileHandle;
use IO::Uncompress::Gunzip;

my($in1,$in2,$out1,$out2,$hash_all,$hash_ids);
GetOptions("i=s" => \$in1,"j=s" => \$in2,"o=s" => \$out1,"p=s" => \$out2, "a" => \$hash_all, "b" => \$hash_ids);
usage() if(!$in1 || !$in2 || !$out1 || !$out2);

# Global vars
# read file
my %h;
my @idlist;

# Filehandles for mates are valid for all functions
# define filehandles for printing mates
if ($out1 =~ /.gz$/) {
  open(MATE1, "| gzip -c > $out1") || die "Can't open file";
} else {
  open(MATE1, "> $out1") or die $!;
}
if ($out2 =~ /.gz$/) {
  open(MATE2, "| gzip -c > $out2") || die "Can't open file";
} else {
  open(MATE2, "> $out2") or die $!;
}

# Choose function to run
if ($hash_all) {
  print "Hashing entire sequence";
  resync_hash_all();
} elsif ($hash_ids) {
  print "Hashing ids only";
  resync_hash_ids();
} else {
  resync_default();
}

sub resync_default {
  my ($s1, $s2, $seq1, $seq2, $id1, $id2, $rid1, $rid2);
  # define filehandles for reading input once again
  if ($in1 =~ /.gz$/) {
    open(INMATE1, "gunzip -c $in1 |") || die "Can't open file";
  } else {
    open(INMATE1, $in1) || die "Can't open file";
  }
  if ($in2 =~ /.gz$/) {
    open(INMATE2, "gunzip -c $in2 |") || die "Can't open file";
  } else {
    open(INMATE2, $in2) || die "Can't open file";
  }
  while (1) {
    $s1 = nextSeq(*INMATE1);
    $s2 = nextSeq(*INMATE2);
    if (not $s1) {
      last;
    }
    ($id1, $seq1) = split /\n/, $s1;
    ($id2, $seq2) = split /\n/, $s2;
    ($rid1) = $id1 =~ /(\w+)/;
    ($rid2) = $id2 =~ /(\w+)/;
    if ($rid1 ne $rid2) {
      print "WARNING: ids differ: '$rid1' ne '$rid2'; quitting\n";
      last;
    }
    if (length($seq1) > 0 and length($seq2) > 0) {
      print MATE1 $s1;
      print MATE2 $s2;
    }
  }
  close(INMATE1);
  close(INMATE2);
}

sub resync_hash_all {
  # hash both mates
  hashFile($in1,"m1");
  hashFile($in2,"m2");
  # loop over hash and print to each output
  for my $id (keys %h) {
    if($h{$id}{'m1'}{'seq'} && $h{$id}{'m2'}{'seq'}) {
      print MATE1 printRead($h{$id}{'m1'});
      print MATE2 printRead($h{$id}{'m2'});
    }
  }
}

sub resync_hash_ids {
  # hash both mates
  hashFile($in1,"m1");
  hashFile($in2,"m2");
  # define filehandles for reading input once again
  if ($in1 =~ /.gz$/) {
    open(INMATE1, "gunzip -c $in1 |") || die "Can't open file";
  } else {
    open(INMATE1, $in1) || die "Can't open file";
  }
  if ($in2 =~ /.gz$/) {
    open(INMATE2, "gunzip -c $in2 |") || die "Can't open file";
  } else {
    open(INMATE2, $in2) || die "Can't open file";
  }
  my ($s1, $s2);
  for my $id (@idlist) {
    if($h{$id}{'m1'} && $h{$id}{'m2'}) {
      $s1 = nextSeq(*INMATE1, $id);
      $s2 = nextSeq(*INMATE2, $id);
      print MATE1 $s1;
      print MATE2 $s2;
    }
  }
  close(INMATE1);
  close(INMATE2);
}

close(MATE1);
close(MATE2);

# Get next wanted sequence from input
sub nextSeq {
  my ($fh, $wantid) = @_;
  my ($id, $rid, $seq, $qual);
  while (1) {
    $id = <$fh>;
    if (eof) {
      return undef;
    }
    chomp $id;
    ($rid,undef) = $id =~ m/^(.*?)[\s\/][12].*?$/;
    $seq = <$fh>; chomp($seq);
    <$fh>; # Jump one row...
    $qual = <$fh>; chomp($qual);
    if (!$wantid) {
      last;
    }
    if ($rid eq $wantid) {
      last;
    }
  }
  return "$id\n$seq\n+\n$qual\n";
}

# print the fastq read
sub printRead {
  my %r=%{$_[0]};
  return "$r{'id'}\n$r{'seq'}\n+\n$r{'qual'}\n";
}


# set id to hash
sub hashFile {
  my($file,$mate)=@_;
  my($id, $rid, $seq, $qual);
  if ($file =~ /.gz$/) {
    open(FH, "gunzip -c $file |") || die "Can't open file";
  } else {
    open(FH, $file) || die "Can't open file";
  }
  while(<FH>) {
    chomp;
    $id = $_;
    ($rid,undef) = $id =~ m/^(.*?)[\s\/][12].*?$/;
    $seq = <FH>; chomp($seq);
      <FH>; # Jump one row...
    $qual = <FH>; chomp($qual);
    if ($hash_all) {
      if(length($seq) != 0) {
	$h{$rid}{$mate}{'id'}=$id;
	$h{$rid}{$mate}{'seq'}=$seq;
	$h{$rid}{$mate}{'qual'}=$qual;
      }
    } else {
      if ($mate eq "m1") {
	push @idlist, $rid;
      }
      if(length($seq) != 0) {
	$h{$rid}{$mate}{'id'}=$id;
      }
    }
  }
  close(FH);
}


# usage information
sub usage {
  print "\nUsage: $0\n
-a     Hash entire reads (default: false)
-b     Hash only ids (default: false)
-i     Input for mate1
-j     Input for mate2
-o     Output for mate1
-p     Output for mate2\n\n";
  exit(1);
}
