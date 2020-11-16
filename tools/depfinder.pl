#!/usr/bin/env perl
#==============================================================================#
# DEPFINDER
#------------------------------------------------------------------------------#
# Author:  Edward Higgins <ed.higgins@york.ac.uk>
#------------------------------------------------------------------------------#
# Version: 0.1.1, 2020-10-20
#------------------------------------------------------------------------------#
# This code is distributed under the MIT license.
#==============================================================================#
use v5.24;
use warnings;
use GraphViz;

sub main {
    my $dir = $ARGV[0] || ".";
    my @files = glob "$dir/*.m";
    my %fnames = ();

    my @functions = ();
    for my $file (@files) {
        my $name = get_fname($file);
        $fnames{$name} = $file;
        push @functions, $name; 
    }

    my $graph = GraphViz->new(rankdir=>"LR");
    $graph->add_node($_, label => $_ . " [" . `wc -l ${fnames{$_}} | awk '{printf \$1}'` . " lines]") for @functions;

    my %calls = ();
    for my $file (@files) {
        my $func = get_fname($file);
        $calls{$func} = {};
        calls: for my $calls (@functions) {
            next if $calls eq $func;
            open my $fh, $file or die $!;
            lines: for my $line (<$fh>) {
                $line =~ s/%.*$//;
                $line =~ s/".*?"/"."/;
                $line =~ s/'.*?'/'.'/;

                if ($line =~ /$calls/) {
                    $graph->add_edge($func, $calls);
                    last lines;
                }
            }
            close $fh;
        }
    }

    open my $fh, "> callgraph.png" or die $!; 
    print $fh $graph->as_png;
    close $fh;
}

sub get_fname {
    my $fname = shift;
    $fname =~ s/.*\/(\w+)\.m$/$1/;
    $fname =~ s/\d+$//g;
    return $fname;
}

&main();

__END__
# Below is stub documentation for your module. You'd better edit it!

=head1 NAME

depfinder - <short description of the program>

=head1 SYNOPSIS

<example usage>

=head1 BUGS

No known bugs

=head1 AUTHOR

Edward Higgins <ed.higgins@york.ac.uk>

=cut
