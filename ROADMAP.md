ROADMAP for C-Blosc2
====================

C-Blosc2 is the new iteration of C-Blosc 1.x series, adding more features and better documentation.
This document lists the goals for a production release of C-Blosc2.

Naming conventions
------------------

Throughout this document we are going to use the next conventions:

* `C-Blosc1` will be used instead of the official `C-Blosc` name for referring to the 1.x series of the library.  This is to make the distinction between the C-Blosc 2.x series and C-Blosc 1.x series more explicit.
 

Existing features
-----------------

Right now (January 2019), the next features are already implemented (although they may require some refactoring or most tests):

* 64-bit containers.  The first-class container in C-Blosc2 is the `super-chunk` or, for brevity, `schunk`, that is made by smaller containers which are essentially C-Blosc1 32-bit containers.  The super-chunk can be backed or not by another container which is called a `frame` (see later).

* More filters: besides `shuffle` and `bitshuffle` already present in C-Blosc1, C-Blosc2 already implements:
  
  - `delta`: the stored blocks inside a chunk are diff'ed with respect to first block in the chunk.  The idea is that, in some situations, the diff will have more zeros than the original data, leading to better compression.
  
  - `trun_prec`: it zeroes the least significant bits of the matissa of float32 and float64 types.  When combined with the `shuffle` or `bitshuffle` filter, this leads to more contiguous zeros, which are compressed better.
  
* A filter pipeline: the different filters can be pipelined so that the output of one can the input for the other.  A possible example is a `delta` followed by `shuffle`, or as described above, `trunc_prec` followed by `bitshuffle`.

* SIMD support for ARM (NEON): this allows for faster operation on ARM architectures, which are meant to be considered first-class citizens for C-Blosc2.  Only `shuffle` is supported right now, but the idea is to implement `bitshuffle` for NEON too.  Other implementations (PowerPC?) would be desirable, but not prioritary.

* Dictionaries: when a block is going to be compressed, C-Blosc2 can use a previously made dictionary (stored in the header of the super-chunk) for compressing all the blocks that are part of the chunks.  This usually improves the compression ratio, as well as the decompression speed, at the expense of a (small) overhead in compression speed.  Currently, it is only supported in the `zstd` codec, but would be nice to extend it to `lz4` and `blosclz` at least.

* Frames: allow to store super-chunks contiguously, either on-disk or in-memory.  When a super-chunk is backed by a frame, instead of storing all the chunks sparsely in-memory, they are serialized inside the frame container.  The frame can be stored on-disk too, meaning that persistence of super-chunks is supported.

* Meta-layers: optionally, the user can add meta-data for different uses and in different layers.  For example, one may think on providing a meta-layer for [NumPy](http://www.numpy.org) so that most of the meta-data for it is stored in a meta-layer; then, one can place another meta-layer on top of the latter can add more high-level info (e.g. geo-spatial, meteorological...), if desired. 


Actions to be done
------------------

* API improvements: make the current API as consistent and minimal as possible.  For example, right now it is possible to access the frame object via specific calls (`blosc2_frame_XXX()`), but perhaps it would be better to let it to be accessed just via super-chunk calls (`blosc2_schunk_XXX()`).
  
* Lock support for super-chunks: when different processes are accessing concurrently to super-chunks, make them to sync properly by using locks, either on-disk (frame-backed super-chunks), or in-memory.

* Documentation: utterly important for attracting new users and making the life easier for existing ones.  Important points to have in mind here:

  - Quality of API docstrings: is the mission of the functions or data structures clearly and succintly explained? Are all the parameters explained?  Is the return value explained?  What are the possible errors that can be returned?
  
  - Markup system: besides the API docstrings, more documentation materials should be provided, like tutorials or a book about Blosc (or at least, the beginnings of it).  Due to its adoption in GitHub and Jupyter notebooks, one of the most extended and useful markup systems is MarkDown, so this should also be the first candidate to use here. 
  
  - Quality of the rendering: it would be desirable to use a rendering system that offers high quality HTML and PDF documents.  [Sphinx](http://www.sphinx-doc.org/en/master/) is perhaps one of the best rendering engines out-there.  Find out whether this can be used in combination for C-based docstrings.
  
* Wrappers for other languages: Python and Java are the most obvious candidates, but others like R or Julia would be nice to have.  Still not sure if these should be produced and maintained by the Blosc core team, or leave them for third-party players that would be interested.


Outreaching
-----------

* Improve the Blosc website: create a nice, modern-looking and easy to navigate website so that new potential users can see at first glimpse what's Blosc all about and power-users can access the documentation part easily.  Ideally, a site-only search box would be great (sphix-based docs would offer this for free).

* Attend to meetings: it is very important to plan going to conferences for advertising C-Blosc2 and meeting people in-person.  Questions is, which meetings?  When on the Python arena, the answer would be quite clear, but for general C libraries like C-Blosc2, I am not certain which ones are the most suited. 
  
* Other outreaching activities would be to produce videos of the kind 'Blosc in 10 minutes', but not sure if this would be interesting for potential Blosc users (probably short tutorials in docs would be better suited).

